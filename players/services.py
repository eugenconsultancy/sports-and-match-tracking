"""
Service layer for players app.
Contains business logic for player statistics, market value tracking,
career analysis, and search functionality.
"""
import logging
from django.db import transaction
from django.db.models import Q, Sum, Avg, Count, F, Case, When, IntegerField, DecimalField
from django.utils import timezone
from django.core.cache import cache

logger = logging.getLogger(__name__)


class PlayerService:
    """Service class for player-related business logic."""

    @staticmethod
    def get_player_by_slug(slug):
        """Get player by slug with related data."""
        from .models import Player

        return Player.objects.filter(slug=slug).select_related(
            'current_team'
        ).first()

    @staticmethod
    def get_player_full_profile(player_id):
        """
        Get a complete player profile with all related data.
        Returns cached result for performance.
        """
        from .models import Player, PlayerStats, PlayerMatchStats, TransferHistory

        cache_key = f'player_full_profile:{player_id}'
        cached = cache.get(cache_key)

        if cached:
            return cached

        player = Player.objects.select_related(
            'current_team'
        ).prefetch_related(
            'season_stats__season',
            'season_stats__team',
            'match_stats__match__home_team',
            'match_stats__match__away_team',
            'transfers__from_team',
            'transfers__to_team',
        ).get(id=player_id)

        profile = {
            'player': player,
            'season_stats': player.season_stats.all()[:5],
            'recent_matches': player.match_stats.select_related(
                'match__home_team', 'match__away_team'
            ).order_by('-match__kickoff_time')[:20],
            'transfers': player.transfers.all().order_by('-transfer_date'),
            'career_totals': PlayerService.calculate_career_totals(player),
        }

        cache.set(cache_key, profile, 300)  # Cache for 5 minutes
        return profile

    @staticmethod
    def calculate_career_totals(player):
        """Calculate career totals for a player across all seasons."""
        from .models import PlayerStats

        totals = PlayerStats.objects.filter(
            player=player
        ).aggregate(
            total_appearances=Sum('appearances'),
            total_minutes=Sum('minutes_played'),
            total_goals=Sum('goals'),
            total_assists=Sum('assists'),
            total_yellow_cards=Sum('yellow_cards'),
            total_red_cards=Sum('red_cards'),
            total_shots=Sum('shots_total'),
            total_shots_on_target=Sum('shots_on_target'),
            average_rating=Avg('average_rating'),
            seasons_played=Count('id'),
        )

        # Calculate goals per game
        if totals['total_appearances'] and totals['total_appearances'] > 0:
            totals['goals_per_game'] = round(
                totals['total_goals'] / totals['total_appearances'], 2
            )
        else:
            totals['goals_per_game'] = 0

        # Calculate assists per game
        if totals['total_appearances'] and totals['total_appearances'] > 0:
            totals['assists_per_game'] = round(
                totals['total_assists'] / totals['total_appearances'], 2
            )
        else:
            totals['assists_per_game'] = 0

        # Calculate goal contributions
        totals['goal_contributions'] = (
            (totals['total_goals'] or 0) + (totals['total_assists'] or 0)
        )

        return totals

    @staticmethod
    def get_top_scorers(competition_season_id=None, team_id=None, limit=10):
        """
        Get top goal scorers with optional filters.
        Can filter by season and/or team.
        """
        from .models import PlayerStats

        filters = {}
        if competition_season_id:
            filters['season_id'] = competition_season_id
        if team_id:
            filters['team_id'] = team_id

        cache_key = f'top_scorers:{competition_season_id}:{team_id}:{limit}'
        cached = cache.get(cache_key)

        if cached:
            return cached

        top_scorers = PlayerStats.objects.filter(
            **filters
        ).select_related(
            'player', 'team'
        ).annotate(
            total_goals=Sum('goals')
        ).order_by('-total_goals')[:limit]

        result = []
        for idx, stat in enumerate(top_scorers, 1):
            result.append({
                'rank': idx,
                'player_id': str(stat.player_id),
                'player_name': stat.player.full_name,
                'player_image': stat.player.image_url,
                'team_name': stat.team.name,
                'team_logo': stat.team.logo_url,
                'goals': stat.total_goals,
                'appearances': stat.appearances,
                'assists': stat.assists,
                'minutes_played': stat.minutes_played,
            })

        cache.set(cache_key, result, 600)  # Cache for 10 minutes
        return result

    @staticmethod
    def get_top_assisters(competition_season_id=None, team_id=None, limit=10):
        """Get top assist providers with optional filters."""
        from .models import PlayerStats

        filters = {}
        if competition_season_id:
            filters['season_id'] = competition_season_id
        if team_id:
            filters['team_id'] = team_id

        cache_key = f'top_assisters:{competition_season_id}:{team_id}:{limit}'
        cached = cache.get(cache_key)

        if cached:
            return cached

        top_assisters = PlayerStats.objects.filter(
            **filters
        ).select_related(
            'player', 'team'
        ).annotate(
            total_assists=Sum('assists')
        ).order_by('-total_assists')[:limit]

        result = []
        for idx, stat in enumerate(top_assisters, 1):
            result.append({
                'rank': idx,
                'player_id': str(stat.player_id),
                'player_name': stat.player.full_name,
                'player_image': stat.player.image_url,
                'team_name': stat.team.name,
                'team_logo': stat.team.logo_url,
                'assists': stat.total_assists,
                'appearances': stat.appearances,
                'goals': stat.goals,
            })

        cache.set(cache_key, result, 600)
        return result

    @staticmethod
    def get_top_rated_players(competition_season_id=None, min_appearances=5, limit=10):
        """Get highest rated players with minimum appearances threshold."""
        from .models import PlayerStats

        filters = {
            'appearances__gte': min_appearances,
        }
        if competition_season_id:
            filters['season_id'] = competition_season_id

        top_rated = PlayerStats.objects.filter(
            **filters
        ).select_related(
            'player', 'team'
        ).order_by('-average_rating')[:limit]

        result = []
        for idx, stat in enumerate(top_rated, 1):
            result.append({
                'rank': idx,
                'player_id': str(stat.player_id),
                'player_name': stat.player.full_name,
                'player_image': stat.player.image_url,
                'team_name': stat.team.name,
                'team_logo': stat.team.logo_url,
                'rating': float(stat.average_rating) if stat.average_rating else None,
                'appearances': stat.appearances,
                'goals': stat.goals,
                'assists': stat.assists,
            })

        return result

    @staticmethod
    def get_players_by_position(position, limit=50):
        """Get players filtered by position."""
        from .models import Player

        return Player.objects.filter(
            position=position,
            is_active=True
        ).select_related('current_team').order_by('-market_value')[:limit]

    @staticmethod
    def get_players_by_team(team_id, position=None, limit=50):
        """Get players for a specific team, optionally filtered by position."""
        from .models import Player

        filters = {
            'current_team_id': team_id,
            'is_active': True,
        }
        if position:
            filters['position'] = position

        return Player.objects.filter(
            **filters
        ).order_by('position', 'last_name')[:limit]

    @staticmethod
    def search_players(query, limit=20):
        """Search players by name, nationality, or position."""
        from .models import Player

        return Player.objects.filter(
            Q(full_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(nationality__icontains=query)
        ).filter(
            is_active=True
        ).select_related('current_team').order_by('-market_value')[:limit]

    @staticmethod
    def get_player_match_history(player_id, season_id=None, limit=50):
        """Get match history for a player, optionally filtered by season."""
        from .models import PlayerMatchStats

        filters = {'player_id': player_id}
        if season_id:
            filters['match__competition_season_id'] = season_id

        return PlayerMatchStats.objects.filter(
            **filters
        ).select_related(
            'match__home_team', 'match__away_team'
        ).order_by('-match__kickoff_time')[:limit]

    @staticmethod
    def get_player_form(player_id, last_n=5):
        """
        Get a player's form based on ratings from last N matches.
        Returns list of ratings and trend indicator.
        """
        from .models import PlayerMatchStats

        recent = PlayerMatchStats.objects.filter(
            player_id=player_id,
            rating__isnull=False
        ).order_by('-match__kickoff_time')[:last_n]

        if not recent:
            return {'ratings': [], 'average': None, 'trend': 'stable'}

        ratings = [float(r.rating) for r in recent]

        # Calculate trend
        if len(ratings) >= 2:
            recent_avg = sum(ratings[:len(ratings)//2]) / (len(ratings)//2)
            older_avg = sum(ratings[len(ratings)//2:]) / (len(ratings) - len(ratings)//2)
            if recent_avg > older_avg + 0.2:
                trend = 'improving'
            elif recent_avg < older_avg - 0.2:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'

        return {
            'ratings': ratings,
            'average': round(sum(ratings) / len(ratings), 2),
            'trend': trend,
            'best': max(ratings),
            'worst': min(ratings),
        }

    @staticmethod
    def get_player_transfer_history(player_id):
        """Get complete transfer history for a player."""
        from .models import TransferHistory

        return TransferHistory.objects.filter(
            player_id=player_id
        ).select_related(
            'from_team', 'to_team'
        ).order_by('-transfer_date')

    @staticmethod
    @transaction.atomic
    def update_market_value(player_id, new_value, currency='EUR'):
        """Update a player's market value."""
        from .models import Player

        player = Player.objects.select_for_update().get(id=player_id)
        old_value = player.market_value

        player.market_value = new_value
        player.market_value_currency = currency
        player.save(update_fields=['market_value', 'market_value_currency', 'updated_at'])

        # Invalidate caches
        cache.delete_pattern(f'player_full_profile:{player_id}')
        cache.delete_pattern('top_scorers:*')
        cache.delete_pattern('top_*')

        logger.info(
            f"Updated market value for {player.full_name}: "
            f"{old_value} -> {new_value} {currency}"
        )

        return player

    @staticmethod
    @transaction.atomic
    def record_transfer(player_id, to_team_id, transfer_date, transfer_fee=None,
                        from_team_id=None, is_loan=False, contract_until=None):
        """Record a player transfer."""
        from .models import Player, TransferHistory
        from teams.models import Team

        player = Player.objects.select_for_update().get(id=player_id)
        to_team = Team.objects.get(id=to_team_id)

        if not from_team_id:
            from_team_id = player.current_team_id

        # Create transfer record
        transfer = TransferHistory.objects.create(
            player=player,
            from_team_id=from_team_id,
            to_team=to_team,
            transfer_date=transfer_date,
            transfer_fee=transfer_fee,
            transfer_fee_currency='EUR',
            is_loan=is_loan,
            contract_until=contract_until,
        )

        # Update player's current team
        player.current_team = to_team
        player.jersey_number = None  # Reset jersey number for new team
        player.save(update_fields=['current_team', 'jersey_number', 'updated_at'])

        # Invalidate caches
        cache.delete_pattern(f'player_full_profile:{player_id}')
        cache.delete_pattern(f'team_players:{from_team_id}')
        cache.delete_pattern(f'team_players:{to_team_id}')

        logger.info(
            f"Recorded transfer: {player.full_name} from "
            f"{transfer.from_team_id} to {transfer.to_team_id}"
        )

        return transfer

    @staticmethod
    @transaction.atomic
    def create_player_stats(player_id, season_id, team_id, **stats_data):
        """Create or update player season statistics."""
        from .models import PlayerStats

        stats, created = PlayerStats.objects.update_or_create(
            player_id=player_id,
            season_id=season_id,
            team_id=team_id,
            defaults=stats_data
        )

        # Invalidate caches
        cache.delete_pattern(f'player_full_profile:{player_id}')
        cache.delete_pattern('top_scorers:*')
        cache.delete_pattern('top_assisters:*')
        cache.delete_pattern('top_rated:*')

        return stats, created

    @staticmethod
    @transaction.atomic
    def create_match_stats(match_id, player_id, team_id, **stats_data):
        """Create or update player match statistics."""
        from .models import PlayerMatchStats

        stats, created = PlayerMatchStats.objects.update_or_create(
            match_id=match_id,
            player_id=player_id,
            defaults={
                'team_id': team_id,
                **stats_data
            }
        )

        logger.debug(
            f"Updated match stats for player {player_id} in match {match_id}"
        )

        return stats, created

    @staticmethod
    def get_players_with_expiring_contracts(months=6, limit=20):
        """Get players whose contracts are expiring soon."""
        from .models import TransferHistory
        from django.utils import timezone
        from datetime import timedelta

        cutoff = timezone.now().date() + timedelta(days=30 * months)

        # Get most recent transfer/contract for each player
        recent_transfers = TransferHistory.objects.filter(
            contract_until__isnull=False,
            contract_until__lte=cutoff,
            contract_until__gte=timezone.now().date(),
        ).select_related(
            'player', 'to_team'
        ).order_by('contract_until')[:limit]

        result = []
        for transfer in recent_transfers:
            days_left = (transfer.contract_until - timezone.now().date()).days
            result.append({
                'player_id': str(transfer.player_id),
                'player_name': transfer.player.full_name,
                'player_image': transfer.player.image_url,
                'current_team': transfer.to_team.name,
                'contract_until': transfer.contract_until,
                'days_left': days_left,
                'market_value': transfer.player.market_value,
            })

        return result

    @staticmethod
    def get_most_valuable_players(limit=20, nationality=None):
        """Get players sorted by market value."""
        from .models import Player

        filters = {'is_active': True, 'market_value__isnull': False}
        if nationality:
            filters['nationality'] = nationality

        return Player.objects.filter(
            **filters
        ).select_related('current_team').order_by('-market_value')[:limit]

    @staticmethod
    def get_similar_players(player_id, limit=10):
        """
        Find similar players based on position, nationality, age, and market value.
        """
        from .models import Player

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return []

        # Find players with same position
        similar = Player.objects.filter(
            position=player.position,
            is_active=True
        ).exclude(
            id=player_id
        )

        # Prioritize by market value proximity and nationality
        if player.market_value:
            similar = similar.annotate(
                value_diff=Case(
                    When(market_value__isnull=True, then=999999999),
                    default=F('market_value') - player.market_value,
                    output_field=DecimalField()
                )
            ).order_by('value_diff')
        else:
            similar = similar.order_by('?')

        return similar.select_related('current_team')[:limit]

    @staticmethod
    def get_team_squad_statistics(team_id, season_id=None):
        """
        Get comprehensive squad statistics for a team.
        Includes top scorers, most appearances, cards, etc.
        """
        from .models import PlayerStats

        filters = {'team_id': team_id}
        if season_id:
            filters['season_id'] = season_id

        stats = PlayerStats.objects.filter(**filters).aggregate(
            total_goals=Sum('goals'),
            total_assists=Sum('assists'),
            total_yellow_cards=Sum('yellow_cards'),
            total_red_cards=Sum('red_cards'),
            total_minutes=Sum('minutes_played'),
            avg_rating=Avg('average_rating'),
            players_used=Count('player_id', distinct=True),
        )

        return {
            'total_goals': stats['total_goals'] or 0,
            'total_assists': stats['total_assists'] or 0,
            'total_yellow_cards': stats['total_yellow_cards'] or 0,
            'total_red_cards': stats['total_red_cards'] or 0,
            'total_minutes': stats['total_minutes'] or 0,
            'average_rating': round(float(stats['avg_rating']), 2) if stats['avg_rating'] else None,
            'players_used': stats['players_used'] or 0,
        }

    @staticmethod
    def get_player_head_to_head(player_id, opponent_team_id, limit=10):
        """Get a player's performance record against a specific opponent."""
        from .models import PlayerMatchStats

        performances = PlayerMatchStats.objects.filter(
            player_id=player_id,
            match__away_team_id=opponent_team_id,
            team=F('match__home_team')
        ) | PlayerMatchStats.objects.filter(
            player_id=player_id,
            match__home_team_id=opponent_team_id,
            team=F('match__away_team')
        )

        performances = performances.select_related(
            'match'
        ).order_by('-match__kickoff_time')[:limit]

        record = {
            'matches': [],
            'total_goals': 0,
            'total_assists': 0,
            'total_yellow': 0,
            'total_red': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'average_rating': 0,
        }

        ratings_sum = 0
        ratings_count = 0

        for perf in performances:
            # Determine if player's team won
            if perf.team_id == perf.match.home_team_id:
                if perf.match.home_score > perf.match.away_score:
                    record['wins'] += 1
                elif perf.match.home_score == perf.match.away_score:
                    record['draws'] += 1
                else:
                    record['losses'] += 1
            else:
                if perf.match.away_score > perf.match.home_score:
                    record['wins'] += 1
                elif perf.match.away_score == perf.match.home_score:
                    record['draws'] += 1
                else:
                    record['losses'] += 1

            record['total_goals'] += perf.goals
            record['total_assists'] += perf.assists
            record['total_yellow'] += 1 if perf.yellow_card else 0
            record['total_red'] += 1 if perf.red_card else 0

            if perf.rating:
                ratings_sum += float(perf.rating)
                ratings_count += 1

            record['matches'].append({
                'match_id': str(perf.match_id),
                'date': perf.match.kickoff_time,
                'goals': perf.goals,
                'assists': perf.assists,
                'rating': float(perf.rating) if perf.rating else None,
            })

        if ratings_count > 0:
            record['average_rating'] = round(ratings_sum / ratings_count, 2)

        return record

    @staticmethod
    def invalidate_player_cache(player_id):
        """Invalidate all cached data for a player."""
        cache.delete_pattern(f'player_full_profile:{player_id}')
        cache.delete_pattern(f'player_form:{player_id}')
        cache.delete_pattern('top_scorers:*')
        cache.delete_pattern('top_assisters:*')
        cache.delete_pattern('top_rated:*')
        cache.delete_pattern('most_valuable:*')
        cache.delete_pattern('search_players:*')

    @staticmethod
    def get_player_stat_comparison(player_ids):
        """
        Compare statistics between multiple players.
        Useful for player comparison widgets.
        """
        from .models import Player, PlayerStats

        if len(player_ids) < 2:
            return None

        players = Player.objects.filter(id__in=player_ids).select_related('current_team')

        # Get current season stats for all players
        current_stats = PlayerStats.objects.filter(
            player_id__in=player_ids,
            season__is_current=True
        )

        comparison = {
            'players': [],
            'metrics': [
                'appearances', 'goals', 'assists', 'minutes_played',
                'yellow_cards', 'red_cards', 'average_rating',
            ],
        }

        for player in players:
            player_stats = current_stats.filter(player=player).first()
            comparison['players'].append({
                'id': str(player.id),
                'name': player.full_name,
                'image': player.image_url,
                'team': player.current_team.name if player.current_team else None,
                'position': player.position,
                'stats': {
                    'appearances': player_stats.appearances if player_stats else 0,
                    'goals': player_stats.goals if player_stats else 0,
                    'assists': player_stats.assists if player_stats else 0,
                    'minutes_played': player_stats.minutes_played if player_stats else 0,
                    'yellow_cards': player_stats.yellow_cards if player_stats else 0,
                    'red_cards': player_stats.red_cards if player_stats else 0,
                    'average_rating': float(player_stats.average_rating) if player_stats and player_stats.average_rating else 0,
                },
            })

        return comparison
"""
Management command to seed the database with sample data.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample sports data'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create competitions
        competitions = self._create_competitions()
        
        # Create teams
        teams = self._create_teams()
        
        # Create venues
        venues = self._create_venues()
        
        # Create players
        players = self._create_players(teams)
        
        # Create seasons
        season = self._create_season(competitions['premier_league'])
        
        # Create matches
        matches = self._create_matches(teams, season, venues)
        
        # Create match events
        self._create_match_events(matches, players)
        
        # Create standings
        self._create_standings(season, teams)
        
        # Create polls
        self._create_polls(matches, teams)
        
        # Create news articles
        self._create_news()
        
        # Create admin user
        self._create_admin_user()
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
    
    def _create_competitions(self):
        from competitions.models import Competition
        
        competitions = {}
        
        competitions['premier_league'] = Competition.objects.create(
            name='Premier League',
            short_name='EPL',
            slug='premier-league',
            competition_type='league',
            tier=1,
            country='England',
            country_flag='https://flagcdn.com/w320/gb-eng.png',
            logo_url='https://example.com/premier-league.png',
            primary_color='#3d195b',
            secondary_color='#f7005a',
            is_active=True,
        )
        
        competitions['la_liga'] = Competition.objects.create(
            name='La Liga',
            short_name='La Liga',
            slug='la-liga',
            competition_type='league',
            tier=1,
            country='Spain',
            country_flag='https://flagcdn.com/w320/es.png',
            logo_url='https://example.com/la-liga.png',
            primary_color='#ff4b44',
            secondary_color='#004a98',
            is_active=True,
        )
        
        competitions['world_cup'] = Competition.objects.create(
            name='FIFA World Cup',
            short_name='WC',
            slug='fifa-world-cup',
            competition_type='international',
            tier=1,
            country='International',
            country_flag='https://flagcdn.com/w320/un.png',
            logo_url='https://example.com/world-cup.png',
            primary_color='#326295',
            secondary_color='#ffffff',
            is_active=True,
        )
        
        return competitions
    
    def _create_teams(self):
        from teams.models import Team
        
        teams = {}
        
        epl_teams = [
            ('Arsenal', 'ARS', 'arsenal', 'London'),
            ('Manchester City', 'MCI', 'manchester-city', 'Manchester'),
            ('Liverpool', 'LIV', 'liverpool', 'Liverpool'),
            ('Manchester United', 'MUN', 'manchester-united', 'Manchester'),
            ('Chelsea', 'CHE', 'chelsea', 'London'),
            ('Tottenham', 'TOT', 'tottenham', 'London'),
            ('Newcastle', 'NEW', 'newcastle', 'Newcastle'),
            ('Aston Villa', 'AVL', 'aston-villa', 'Birmingham'),
        ]
        
        for name, short, slug, city in epl_teams:
            teams[slug] = Team.objects.create(
                name=name,
                short_name=short,
                slug=slug,
                team_type='club',
                country='England',
                primary_color=f'#{random.randint(0, 0xFFFFFF):06x}',
                founded_year=random.randint(1870, 1920),
                is_active=True,
            )
        
        return teams
    
    def _create_venues(self):
        from teams.models import Venue
        
        venues = {}
        
        venue_data = [
            ('Emirates Stadium', 'emirates-stadium', 'London', 'England', 60704, 51.5549, -0.1084),
            ('Etihad Stadium', 'etihad-stadium', 'Manchester', 'England', 53400, 53.4831, -2.2004),
            ('Anfield', 'anfield', 'Liverpool', 'England', 53394, 53.4308, -2.9608),
            ('Old Trafford', 'old-trafford', 'Manchester', 'England', 74310, 53.4631, -2.2913),
            ('Stamford Bridge', 'stamford-bridge', 'London', 'England', 40834, 51.4817, -0.1910),
        ]
        
        for name, slug, city, country, capacity, lat, lon in venue_data:
            venues[slug] = Venue.objects.create(
                name=name,
                slug=slug,
                city=city,
                country=country,
                capacity=capacity,
                latitude=lat,
                longitude=lon,
            )
        
        return venues
    
    def _create_players(self, teams):
        from players.models import Player
        
        players = []
        
        player_names = [
            ('Bukayo', 'Saka', 'England', 'RW', 'arsenal', 7),
            ('Martin', 'Ødegaard', 'Norway', 'AM', 'arsenal', 8),
            ('Erling', 'Haaland', 'Norway', 'ST', 'manchester-city', 9),
            ('Kevin', 'De Bruyne', 'Belgium', 'CM', 'manchester-city', 17),
            ('Mohamed', 'Salah', 'Egypt', 'RW', 'liverpool', 11),
            ('Virgil', 'van Dijk', 'Netherlands', 'CB', 'liverpool', 4),
            ('Marcus', 'Rashford', 'England', 'LW', 'manchester-united', 10),
            ('Bruno', 'Fernandes', 'Portugal', 'AM', 'manchester-united', 8),
        ]
        
        for first, last, nationality, pos, team_slug, number in player_names:
            player = Player.objects.create(
                first_name=first,
                last_name=last,
                full_name=f'{first} {last}',
                slug=f'{first.lower()}-{last.lower()}',
                nationality=nationality,
                position=pos,
                preferred_foot=random.choice(['left', 'right']),
                jersey_number=number,
                current_team=teams[team_slug],
                height_cm=random.randint(170, 195),
                weight_kg=random.randint(65, 90),
                market_value=random.randint(20000000, 150000000),
                is_active=True,
            )
            players.append(player)
        
        return players
    
    def _create_season(self, competition):
        from competitions.models import Season, Stage
        
        season = Season.objects.create(
            competition=competition,
            name='2025/26',
            slug='2025-26',
            start_date=timezone.now().date() - timedelta(days=30),
            end_date=timezone.now().date() + timedelta(days=300),
            status='live',
            is_current=True,
            total_teams=8,
            total_matches=56,
        )
        
        # Create group stage
        stage = Stage.objects.create(
            season=season,
            name='Regular Season',
            stage_type='group',
            order=1,
            is_active=True,
        )
        
        return season
    
    def _create_matches(self, teams, season, venues):
        from matches.models import Match
        
        team_list = list(teams.values())
        venue_list = list(venues.values())
        matches = []
        
        now = timezone.now()
        
        # Create past finished matches
        for i in range(6):
            for j in range(len(team_list)):
                if i != j:
                    match = Match.objects.create(
                        home_team=team_list[i],
                        away_team=team_list[j],
                        competition_season=season,
                        stage=season.stages.first(),
                        venue=venue_list[i % len(venue_list)],
                        round_number=i + 1,
                        kickoff_time=now - timedelta(days=(6-i)*7, hours=random.randint(0, 3)),
                        status='finished',
                        home_score=random.randint(0, 5),
                        away_score=random.randint(0, 5),
                        home_score_halftime=random.randint(0, 3),
                        away_score_halftime=random.randint(0, 2),
                        minute=90,
                        attendance=random.randint(30000, 70000),
                        referee_name=random.choice(['Michael Oliver', 'Anthony Taylor', 'Paul Tierney']),
                    )
                    matches.append(match)
        
        # Create upcoming matches
        for i in range(len(team_list)):
            for j in range(i+1, min(i+4, len(team_list))):
                match = Match.objects.create(
                    home_team=team_list[i],
                    away_team=team_list[j],
                    competition_season=season,
                    stage=season.stages.first(),
                    venue=venue_list[i % len(venue_list)],
                    round_number=7,
                    kickoff_time=now + timedelta(days=random.randint(1, 14), hours=random.choice([15, 17, 20])),
                    status='scheduled',
                    home_score=0,
                    away_score=0,
                )
                matches.append(match)
        
        # Create one live match
        live_match = Match.objects.create(
            home_team=team_list[0],
            away_team=team_list[1],
            competition_season=season,
            stage=season.stages.first(),
            venue=venue_list[0],
            round_number=7,
            kickoff_time=now - timedelta(minutes=30),
            status='live',
            home_score=1,
            away_score=1,
            home_score_halftime=1,
            away_score_halftime=0,
            minute=65,
            attendance=60000,
            referee_name='Michael Oliver',
        )
        matches.append(live_match)
        
        return matches
    
    def _create_match_events(self, matches, players):
        from matches.models import MatchEvent
        
        for match in matches:
            if match.status in ['finished', 'live']:
                # Create goals
                for goal_num in range(match.home_score):
                    MatchEvent.objects.create(
                        match=match,
                        event_type='goal',
                        minute=random.randint(1, 90),
                        player=random.choice(players[:4]),
                        team=match.home_team,
                        score_home=goal_num + 1,
                        score_away=match.away_score,
                        description=f'Goal! {match.home_team.name} scores!',
                    )
                
                for goal_num in range(match.away_score):
                    MatchEvent.objects.create(
                        match=match,
                        event_type='goal',
                        minute=random.randint(1, 90),
                        player=random.choice(players[4:]),
                        team=match.away_team,
                        score_home=match.home_score,
                        score_away=goal_num + 1,
                        description=f'Goal! {match.away_team.name} scores!',
                    )
    
    def _create_standings(self, season, teams):
        from standings.models import Standing, TeamStanding
        
        stage = season.stages.first()
        
        standing = Standing.objects.create(
            competition_season=season,
            stage=stage,
            standing_type='total',
            is_live=True,
        )
        
        team_list = list(teams.values())
        random.shuffle(team_list)
        
        for position, team in enumerate(team_list, 1):
            TeamStanding.objects.create(
                standing=standing,
                team=team,
                position=position,
                played=random.randint(5, 10),
                wins=random.randint(0, 8),
                draws=random.randint(0, 5),
                losses=random.randint(0, 5),
                goals_for=random.randint(10, 30),
                goals_against=random.randint(5, 20),
                goal_difference=random.randint(-5, 15),
                points=random.randint(5, 25),
                form=''.join(random.choice(['W', 'D', 'L']) for _ in range(5)),
            )
    
    def _create_polls(self, matches, teams):
        from polls.models import Poll, PollOption
        
        team_list = list(teams.values())
        
        for match in matches[:5]:
            poll = Poll.objects.create(
                match=match,
                question='Who will win?',
                start_time=timezone.now(),
                status='active',
                is_featured=match.status == 'live',
            )
            
            # Home win option
            PollOption.objects.create(
                poll=poll,
                label=f'{match.home_team.name} Win',
                team=match.home_team,
                option_type='home',
                sort_order=0,
                vote_count=random.randint(100, 1000),
                percentage=random.uniform(30, 50),
            )
            
            # Draw option
            PollOption.objects.create(
                poll=poll,
                label='Draw',
                team=None,
                option_type='draw',
                sort_order=1,
                vote_count=random.randint(50, 500),
                percentage=random.uniform(15, 30),
            )
            
            # Away win option
            PollOption.objects.create(
                poll=poll,
                label=f'{match.away_team.name} Win',
                team=match.away_team,
                option_type='away',
                sort_order=2,
                vote_count=random.randint(100, 1000),
                percentage=random.uniform(25, 45),
            )
    
    def _create_news(self):
        from news.models import Article, Category, Tag
        
        category = Category.objects.create(
            name='Match Reports',
            slug='match-reports',
            description='Match analysis and reports',
        )
        
        tag = Tag.objects.create(name='Premier League', slug='premier-league')
        
        for i in range(10):
            article = Article.objects.create(
                title=f'Sample Article {i+1}: Exciting Match Action',
                slug=f'sample-article-{i+1}',
                subtitle='Match analysis and highlights',
                body='Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' * 10,
                summary='Brief summary of the article content for preview purposes.',
                category=category,
                status='published',
                published_at=timezone.now() - timedelta(days=i),
                is_featured=i < 3,
                is_breaking=i == 0,
                view_count=random.randint(100, 10000),
                reading_time_minutes=random.randint(3, 8),
                meta_title=f'Sample Article {i+1}',
                meta_description='Article about exciting match action.',
            )
            article.tags.add(tag)
    
    def _create_admin_user(self):
        if not User.objects.filter(email='admin@livescore.com').exists():
            User.objects.create_superuser(
                email='admin@livescore.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write('Created superuser: admin@livescore.com / admin123')
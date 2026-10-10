<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 py-8 space-y-12">
      <!-- Enhanced Hero Header -->
      <div class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-indigo-800 rounded-2xl p-8 md:p-12 text-white shadow-xl">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.3),rgba(255,255,255,0))]"></div>
          <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-yellow-500/20 to-transparent rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-purple-500/20 to-transparent rounded-full blur-3xl"></div>
        </div>

        <div class="relative z-10 text-center">
          <div class="inline-flex items-center gap-3 mb-6">
            <div class="w-16 h-16 bg-white/10 backdrop-blur rounded-2xl flex items-center justify-center">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
          </div>
          <h1 class="text-3xl md:text-5xl font-bold mb-4 tracking-tight">Get in Touch</h1>
          <p class="text-lg md:text-xl text-white/80 max-w-2xl mx-auto leading-relaxed">
            Have questions, feedback, or just want to say hello? We'd love to hear from you!
          </p>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-8">
        <!-- Contact Form - Takes 3 columns -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
            <!-- Form Header -->
            <div class="bg-gradient-to-r from-primary-50 to-blue-50 px-6 py-4 border-b border-gray-100">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h2 class="text-lg font-bold text-gray-900">Send us a Message</h2>
                  <p class="text-xs text-gray-500">Fill out the form below and we'll get back to you shortly</p>
                </div>
              </div>
            </div>

            <!-- Form Body -->
            <div class="p-6">
              <form @submit.prevent="submitForm" class="space-y-5">
                <!-- Name Fields -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1.5">First Name</label>
                    <div class="relative">
                      <div class="absolute left-3 top-1/2 -translate-y-1/2">
                        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                      <input 
                        v-model="form.firstName" 
                        type="text" 
                        required 
                        placeholder="John"
                        class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm" />
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1.5">Last Name</label>
                    <div class="relative">
                      <div class="absolute left-3 top-1/2 -translate-y-1/2">
                        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                      <input 
                        v-model="form.lastName" 
                        type="text" 
                        required 
                        placeholder="Doe"
                        class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm" />
                    </div>
                  </div>
                </div>

                <!-- Email -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Email Address</label>
                  <div class="relative">
                    <div class="absolute left-3 top-1/2 -translate-y-1/2">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <input 
                      v-model="form.email" 
                      type="email" 
                      required 
                      placeholder="you@example.com"
                      class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm" />
                  </div>
                </div>

                <!-- Subject -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject</label>
                  <div class="relative">
                    <div class="absolute left-3 top-1/2 -translate-y-1/2">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                      </svg>
                    </div>
                    <select 
                      v-model="form.subject" 
                      required
                      class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm appearance-none bg-white">
                      <option value="" disabled>Select a topic</option>
                      <option value="general">General Inquiry</option>
                      <option value="support">Technical Support</option>
                      <option value="feedback">Feedback & Suggestions</option>
                      <option value="press">Press & Media</option>
                      <option value="partnership">Partnership Opportunities</option>
                      <option value="other">Other</option>
                    </select>
                    <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Message -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Message</label>
                  <textarea 
                    v-model="form.message" 
                    rows="5" 
                    required
                    placeholder="Tell us how we can help you..."
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 text-sm resize-none"></textarea>
                  <p class="text-xs text-gray-400 mt-1">{{ form.message.length }}/1000 characters</p>
                </div>

                <!-- Submit Button -->
                <button 
                  type="submit" 
                  :disabled="submitting"
                  class="w-full px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-xl hover:from-primary-700 hover:to-primary-800 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-300 disabled:opacity-50 shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30 flex items-center justify-center gap-2">
                  <svg v-if="submitting" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                  {{ submitting ? 'Sending...' : 'Send Message' }}
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Contact Info Sidebar - Takes 2 columns -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Contact Cards -->
          <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
            <div class="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b border-gray-100">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <h2 class="text-lg font-bold text-gray-900">Contact Information</h2>
                  <p class="text-xs text-gray-500">Reach out to us anytime</p>
                </div>
              </div>
            </div>
            
            <div class="p-6 space-y-6">
              <!-- Visit Us -->
              <div class="group flex items-start gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer">
                <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 mb-0.5">Visit Us</p>
                  <p class="text-sm text-gray-600">123 Sports Avenue</p>
                  <p class="text-sm text-gray-600">Digital City, DC 12345</p>
                  <p class="text-xs text-gray-400 mt-1">United States</p>
                </div>
              </div>

              <!-- Email Us -->
              <div class="group flex items-start gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer">
                <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 mb-0.5">Email Us</p>
                  <a href="mailto:support@livescore.com" class="text-sm text-blue-600 hover:text-blue-700 transition-colors block">support@livescore.com</a>
                  <a href="mailto:press@livescore.com" class="text-sm text-blue-600 hover:text-blue-700 transition-colors block">press@livescore.com</a>
                </div>
              </div>

              <!-- Call Us -->
              <div class="group flex items-start gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer">
                <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 mb-0.5">Call Us</p>
                  <a href="tel:+15551234567" class="text-sm text-purple-600 hover:text-purple-700 transition-colors block">+1 (555) 123-4567</a>
                  <p class="text-xs text-gray-400 mt-1">Mon-Fri, 9am-6pm EST</p>
                </div>
              </div>

              <!-- Working Hours -->
              <div class="group flex items-start gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors">
                <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900 mb-0.5">Working Hours</p>
                  <p class="text-sm text-gray-600">Monday - Friday</p>
                  <p class="text-sm text-gray-600">9:00 AM - 6:00 PM EST</p>
                  <p class="text-xs text-gray-400 mt-1">Weekend support via email</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Map Card -->
          <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
            <div class="relative h-64 bg-gray-100">
              <iframe 
                src="https://www.openstreetmap.org/export/embed.html?bbox=-74.0060%2C40.7128%2C-73.9352%2C40.7614&layer=mapnik&marker=40.7370%2C-73.9706" 
                width="100%" 
                height="100%" 
                style="border:0;" 
                allowfullscreen="" 
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
              </iframe>
              <!-- Map Overlay -->
              <div class="absolute bottom-3 left-3 bg-white/90 backdrop-blur rounded-lg px-3 py-1.5 shadow-sm">
                <p class="text-xs font-semibold text-gray-700">📍 LiveScore HQ</p>
              </div>
            </div>
            <div class="p-4 bg-gray-50 border-t border-gray-100">
              <a 
                href="https://www.openstreetmap.org/?mlat=40.7370&mlon=-73.9706#map=14/40.7370/-73.9706" 
                target="_blank"
                class="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1 group">
                View larger map
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- FAQ Quick Links -->
      <div class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8 border border-gray-200">
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">Frequently Asked Questions</h2>
          <p class="text-gray-500">Quick answers to common questions</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto">
          <div v-for="faq in faqs" :key="faq.question"
               class="group bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 cursor-pointer">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-primary-200 transition-colors">
                <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="font-semibold text-gray-900 text-sm mb-1 group-hover:text-primary-600 transition-colors">{{ faq.question }}</p>
                <p class="text-xs text-gray-500">{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Social Media Section -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-primary-600 to-purple-600 px-6 py-4">
          <h2 class="text-xl font-bold text-white text-center">Follow Us on Social Media</h2>
        </div>
        
        <div class="p-8">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <!-- Facebook -->
            <a href="#" 
               class="group flex flex-col items-center gap-3 p-4 rounded-xl hover:bg-blue-50 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
              <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center group-hover:bg-blue-500 group-hover:text-white transition-all duration-300">
                <svg class="w-7 h-7 text-blue-600 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900 text-sm">Facebook</p>
                <p class="text-xs text-gray-500">@LiveScore</p>
              </div>
            </a>

            <!-- Twitter/X -->
            <a href="#" 
               class="group flex flex-col items-center gap-3 p-4 rounded-xl hover:bg-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
              <div class="w-14 h-14 bg-gray-200 rounded-2xl flex items-center justify-center group-hover:bg-gray-900 group-hover:text-white transition-all duration-300">
                <svg class="w-7 h-7 text-gray-700 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900 text-sm">Twitter / X</p>
                <p class="text-xs text-gray-500">@LiveScore</p>
              </div>
            </a>

            <!-- Instagram -->
            <a href="#" 
               class="group flex flex-col items-center gap-3 p-4 rounded-xl hover:bg-pink-50 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
              <div class="w-14 h-14 bg-pink-100 rounded-2xl flex items-center justify-center group-hover:bg-gradient-to-br group-hover:from-pink-500 group-hover:to-purple-600 group-hover:text-white transition-all duration-300">
                <svg class="w-7 h-7 text-pink-600 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zM5.838 12a6.162 6.162 0 1112.324 0 6.162 6.162 0 01-12.324 0zM12 16a4 4 0 110-8 4 4 0 010 8zm4.965-10.405a1.44 1.44 0 112.881.001 1.44 1.44 0 01-2.881-.001z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900 text-sm">Instagram</p>
                <p class="text-xs text-gray-500">@LiveScore</p>
              </div>
            </a>

            <!-- LinkedIn -->
            <a href="#" 
               class="group flex flex-col items-center gap-3 p-4 rounded-xl hover:bg-blue-50 transition-all duration-300 hover:shadow-md hover:-translate-y-1">
              <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center group-hover:bg-blue-700 group-hover:text-white transition-all duration-300">
                <svg class="w-7 h-7 text-blue-700 group-hover:text-white transition-colors" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
              </div>
              <div class="text-center">
                <p class="font-semibold text-gray-900 text-sm">LinkedIn</p>
                <p class="text-xs text-gray-500">@LiveScore</p>
              </div>
            </a>
          </div>
        </div>
      </div>

      <!-- Success Toast (shown after form submission) -->
      <Teleport to="body">
        <Transition name="toast-slide">
          <div v-if="showSuccessToast" 
               class="fixed bottom-8 right-8 z-50 bg-white rounded-2xl shadow-2xl border border-gray-100 p-6 max-w-sm">
            <div class="flex items-start gap-4">
              <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="font-semibold text-gray-900">Message Sent! 🎉</p>
                <p class="text-sm text-gray-500 mt-1">We'll get back to you within 24 hours.</p>
              </div>
              <button @click="showSuccessToast = false" class="text-gray-400 hover:text-gray-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUIStore } from '@/stores/ui'

const uiStore = useUIStore()
const submitting = ref(false)
const showSuccessToast = ref(false)

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  subject: '',
  message: '',
})

const faqs = [
  { question: 'How do I create an account?', answer: 'Click the Sign In button and select Create Account. Fill in your details and verify your email.' },
  { question: 'How accurate are the live scores?', answer: 'Our scores update in real-time from official data providers with minimal delay.' },
  { question: 'Can I customize notifications?', answer: 'Yes! Go to Settings to choose which notifications you want to receive.' },
  { question: 'Is LiveScore free to use?', answer: 'Yes, LiveScore is completely free with optional premium features available.' },
  { question: 'How do I report an issue?', answer: 'Use this contact form or email support@livescore.com directly.' },
  { question: 'Do you have a mobile app?', answer: 'Our mobile app is available on iOS and Android app stores.' },
]

async function submitForm() {
  submitting.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Show success
    showSuccessToast.value = true
    uiStore.showSuccess('Message sent successfully!', 'We\'ll get back to you soon')
    
    // Reset form
    form.value = { firstName: '', lastName: '', email: '', subject: '', message: '' }
    
    // Auto-hide toast
    setTimeout(() => { showSuccessToast.value = false }, 5000)
  } catch (error) {
    uiStore.showError('Failed to send message', 'Please try again')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.toast-slide-enter-active {
  transition: all 0.3s ease-out;
}
.toast-slide-leave-active {
  transition: all 0.2s ease-in;
}
.toast-slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
.toast-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>
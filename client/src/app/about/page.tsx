export default function About() {
  return (
    <div className="min-h-screen bg-black py-12">
      <div className="container mx-auto px-4 max-w-4xl relative z-10">
        <div className="text-center mb-12">
          <div className="glass-card rounded-2xl p-8">
            <h1 className="text-4xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              About Prof. Peter's Students
            </h1>
            <div className="flex justify-center items-center gap-2 mt-4">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              <span className="text-gray-300">The most unconventional educational platform</span>
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
        
        <div className="space-y-8">
          <div className="glass-card rounded-2xl p-8">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🎓</span>
              </div>
              <h2 className="text-2xl font-bold text-white">Meet Peter — your video explainer on demand!</h2>
            </div>
            <p className="text-gray-300 leading-relaxed mb-6">
              Welcome to the most unconventional educational platform on the internet! Prof. Peter's Students 
              brings you the unique teaching style of Peter Griffin from Family Guy, transforming your most 
              complex questions into hilariously simple explanations.
            </p>
            
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-3">
              <span className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center text-sm">⚡</span>
              How it works:
            </h3>
            <div className="grid md:grid-cols-2 gap-4 mb-6">
              <div className="bg-black/30 backdrop-blur-sm rounded-xl p-4 border border-gray-600/30">
                <span className="text-blue-400 font-medium">• Pick a template</span>
                <p className="text-gray-400 text-sm">Choose from Educational, Comedy, or Motivational styles</p>
              </div>
              <div className="bg-black/30 backdrop-blur-sm rounded-xl p-4 border border-gray-600/30">
                <span className="text-purple-400 font-medium">• Type your doubts</span>
                <p className="text-gray-400 text-sm">Ask anything - no topic is too complex or weird</p>
              </div>
              <div className="bg-black/30 backdrop-blur-sm rounded-xl p-4 border border-gray-600/30">
                <span className="text-pink-400 font-medium">• Watch Peter explain</span>
                <p className="text-gray-400 text-sm">Get hilarious yet educational explanations</p>
              </div>
              <div className="bg-black/30 backdrop-blur-sm rounded-xl p-4 border border-gray-600/30">
                <span className="text-orange-400 font-medium">• Share with friends</span>
                <p className="text-gray-400 text-sm">Spread the Peter Griffin wisdom everywhere</p>
              </div>
            </div>
            
            <p className="text-gray-300 leading-relaxed">
              Our AI-powered system uses advanced language models to generate scripts in Peter Griffin's 
              distinctive voice and style, complete with his unique perspective on everything from quantum 
              physics to cooking tips. Whether you're a student, teacher, or just someone who enjoys 
              unconventional explanations, Prof. Peter's Students is here to make learning fun and memorable.
            </p>
          </div>
          
          <div className="glass-card rounded-2xl p-8">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🚀</span>
              </div>
              <h3 className="text-2xl font-bold text-white">Technology</h3>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">🧠</span>
                </div>
                <h4 className="text-white font-semibold mb-2">AI Script Generation</h4>
                <p className="text-gray-400 text-sm">Google's Gemini models for intelligent content creation</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">🎙️</span>
                </div>
                <h4 className="text-white font-semibold mb-2">Voice Synthesis</h4>
                <p className="text-gray-400 text-sm">Advanced text-to-speech for Peter's unique voice</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">⚙️</span>
                </div>
                <h4 className="text-white font-semibold mb-2">Modern Stack</h4>
                <p className="text-gray-400 text-sm">Next.js, TypeScript, and Tailwind CSS</p>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-8">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
                <span className="text-2xl">✨</span>
              </div>
              <h3 className="text-2xl font-bold text-white">Why Choose Prof. Peter's Students?</h3>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-xs">🎯</span>
                  Unique Learning Experience
                </h4>
                <p className="text-gray-400 text-sm mb-4">Learn complex topics through Peter's hilariously simple explanations that make everything memorable.</p>
              </div>
              <div>
                <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center text-xs">⚡</span>
                  Instant Results
                </h4>
                <p className="text-gray-400 text-sm mb-4">Generate educational videos in minutes, not hours - perfect for quick explanations.</p>
              </div>
              <div>
                <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span className="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center text-xs">🌍</span>
                  Easy Sharing
                </h4>
                <p className="text-gray-400 text-sm mb-4">Share your generated videos instantly across social media and with colleagues.</p>
              </div>
              <div>
                <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <span className="w-6 h-6 bg-orange-500 rounded-full flex items-center justify-center text-xs">🎭</span>
                  Entertainment Value
                </h4>
                <p className="text-gray-400 text-sm mb-4">Learning doesn't have to be boring - Peter makes even the driest topics entertaining.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="text-center mt-12">
          <div className="glass-card rounded-2xl p-8">
            <div className="flex justify-center items-center gap-4 mb-4">
              <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>
              <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
            <p className="text-blue-400 font-bold italic text-xl">
              "Welcome to PeterTalks • Where prompts die and videos cry."
            </p>
            <p className="text-gray-400 text-sm mt-2">
              Ready to transform your learning experience? Start generating videos now!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 
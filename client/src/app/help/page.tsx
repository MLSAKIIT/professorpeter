export default function Help() {
  return (
    <div className="min-h-screen bg-gray-900 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-4xl font-bold text-white mb-8 text-center">
          Help & Support
        </h1>
        
        <div className="space-y-8">
          <div className="bg-gray-800 rounded-lg p-8">
            <h2 className="text-2xl font-semibold text-white mb-4">Getting Started</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-white mb-2">1. Choose a Template</h3>
                <p className="text-gray-300">
                  Select from our available templates - Educational, Comedy, or Motivational. 
                  Each template adjusts Peter's tone and style for different types of content.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-white mb-2">2. Enter Your Prompt</h3>
                <p className="text-gray-300">
                  Type your question, topic, or concept in the prompt box. Be as specific or as 
                  vague as you want - Peter will find a way to explain it!
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-white mb-2">3. Generate & Share</h3>
                <p className="text-gray-300">
                  Click "Generate Videos" and wait for Peter to work his magic. Once ready, 
                  you can share your video with a direct link or on social media.
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-8">
            <h2 className="text-2xl font-semibold text-white mb-4">Tips for Better Results</h2>
            <ul className="text-gray-300 space-y-3">
              <li>• Be specific with your topics for more focused explanations</li>
              <li>• Complex subjects work great - Peter loves a challenge!</li>
              <li>• Try different templates for varied explanation styles</li>
              <li>• Keep prompts under 200 characters for optimal results</li>
              <li>• Feel free to ask about anything - no topic is too weird for Peter</li>
            </ul>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-8">
            <h2 className="text-2xl font-semibold text-white mb-4">Troubleshooting</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-white mb-2">Video Generation Takes Too Long</h3>
                <p className="text-gray-300">
                  Videos typically take 2-5 minutes to generate. If it's taking longer, 
                  try refreshing the page or simplifying your prompt.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-white mb-2">Can't Share Video</h3>
                <p className="text-gray-300">
                  Make sure your video has finished generating completely. The share buttons 
                  will appear once the video is ready.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-white mb-2">Audio Not Working</h3>
                <p className="text-gray-300">
                  Check your device's audio settings and ensure your browser allows audio playback. 
                  Some browsers may require user interaction before playing audio.
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-8">
            <h2 className="text-2xl font-semibold text-white mb-4">Frequently Asked Questions</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-white mb-2">Is this the real Peter Griffin?</h3>
                <p className="text-gray-300">
                  No, this is an AI-generated interpretation of Peter Griffin's speaking style and personality. 
                  All content is created using advanced language models.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-white mb-2">Can I use these videos commercially?</h3>
                <p className="text-gray-300">
                  Please check our terms of service for commercial usage guidelines. 
                  Personal and educational use is generally encouraged.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-white mb-2">How accurate are the explanations?</h3>
                <p className="text-gray-300">
                  While Peter tries his best, remember this is for entertainment and educational 
                  purposes. Always verify important information from reliable sources!
                </p>
              </div>
            </div>
          </div>
          
          <div className="text-center bg-gray-800 rounded-lg p-8">
            <h2 className="text-2xl font-semibold text-white mb-4">Still Need Help?</h2>
            <p className="text-gray-300 mb-4">
              Can't find what you're looking for? Peter might be confused too, but we're here to help!
            </p>
            <p className="text-gray-400 italic">
              "Remember, there are no stupid questions... only questions that make Peter think too hard."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 
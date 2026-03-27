"use client";

export default function TweakStudio() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simpsons-yellow">Tweak Studio</h1>
      <p className="text-gray-400">
        Select two scenes and generate a bridging transition with Veo 3.1.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Scene A */}
        <div className="bg-gray-900 border border-gray-800 border-dashed rounded-lg p-8 text-center">
          <p className="text-gray-500">Drop Scene A here</p>
          <p className="text-xs text-gray-600 mt-2">Search and select a scene first</p>
        </div>

        {/* Scene B */}
        <div className="bg-gray-900 border border-gray-800 border-dashed rounded-lg p-8 text-center">
          <p className="text-gray-500">Drop Scene B here</p>
          <p className="text-xs text-gray-600 mt-2">Search and select a scene first</p>
        </div>
      </div>

      {/* Transition prompt */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Transition Prompt
        </label>
        <textarea
          placeholder="e.g. Homer walks through a glowing donut portal from the nuclear plant to the union hall"
          className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-simpsons-yellow transition h-24 resize-none"
        />
      </div>

      <button
        disabled
        className="bg-simpsons-yellow text-black font-semibold px-6 py-3 rounded-lg opacity-50 cursor-not-allowed"
      >
        Generate Bridge (Phase 4)
      </button>
    </div>
  );
}

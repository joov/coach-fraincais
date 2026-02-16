import { ref, onBeforeUnmount } from 'vue'

/**
 * Composable for browser Text-to-Speech using the Web Speech API.
 * Supports male and female French voices based on speaker name.
 */
export function useTTS() {
  const isSpeaking = ref(false)
  const isSupported = ref(typeof window !== 'undefined' && 'speechSynthesis' in window)

  let femaleVoice = null
  let maleVoice = null
  let fallbackVoice = null
  let voicesLoaded = false

  // Common French female first names (lowercase) for heuristic gender detection
  const FEMALE_NAMES = new Set([
    'marie', 'anne', 'sophie', 'isabelle', 'christine', 'léa', 'léa',
    'claire', 'julie', 'nathalie', 'catherine', 'françoise', 'céline',
    'valérie', 'sylvie', 'monique', 'brigitte', 'patricia', 'sandrine',
    'véronique', 'florence', 'caroline', 'émilie', 'charlotte', 'alice',
    'camille', 'lucie', 'manon', 'chloé', 'emma', 'sarah', 'laura',
    'sofia', 'elena', 'rosa', 'maria',
  ])

  // Common French male first names (lowercase)
  const MALE_NAMES = new Set([
    'paul', 'pierre', 'jean', 'jacques', 'marc', 'louis', 'françois',
    'philippe', 'michel', 'nicolas', 'thomas', 'david', 'patrick',
    'christophe', 'éric', 'jules', 'antoine', 'lucas', 'hugo',
    'théo', 'léo', 'gabriel', 'raphaël', 'arthur', 'maxime',
    'alexandre', 'daniel', 'robert', 'bernard', 'henri',
  ])

  // Prefixes that indicate gender
  const FEMALE_PREFIXES = ['mme', 'mme.', 'madame', 'mlle', 'mademoiselle']
  const MALE_PREFIXES = ['m.', 'mr', 'mr.', 'monsieur']

  function loadVoices() {
    if (!isSupported.value || voicesLoaded) return
    const voices = speechSynthesis.getVoices()
    if (voices.length === 0) return

    voicesLoaded = true

    const frVoices = voices.filter((v) => v.lang === 'fr-FR' || v.lang.startsWith('fr'))

    if (frVoices.length === 0) return

    // Try to identify female and male voices by name keywords
    for (const v of frVoices) {
      const nameLower = v.name.toLowerCase()
      const isFemaleVoice =
        nameLower.includes('female') ||
        nameLower.includes('femme') ||
        nameLower.includes('amélie') ||
        nameLower.includes('aurelie') ||
        nameLower.includes('marie') ||
        nameLower.includes('audrey') ||
        nameLower.includes('virginie') ||
        nameLower.includes('léa')
      const isMaleVoice =
        nameLower.includes('male') ||
        nameLower.includes('homme') ||
        nameLower.includes('thomas') ||
        nameLower.includes('nicolas') ||
        nameLower.includes('daniel') ||
        nameLower.includes('pierre')

      if (isFemaleVoice && !femaleVoice) femaleVoice = v
      if (isMaleVoice && !maleVoice) maleVoice = v
    }

    // Fallback: first fr voice
    fallbackVoice = frVoices[0]

    // If we only found one gendered voice, use fallback for the other
    if (!femaleVoice) femaleVoice = fallbackVoice
    if (!maleVoice) maleVoice = fallbackVoice
  }

  if (isSupported.value) {
    loadVoices()
    speechSynthesis.addEventListener('voiceschanged', loadVoices)
  }

  /**
   * Guess the gender from a speaker label like "Léa", "M. Merle", "Mme Dupuis".
   * Returns 'female', 'male', or null.
   */
  function guessGender(speaker) {
    if (!speaker) return null
    const parts = speaker.trim().toLowerCase().split(/[\s.]+/).filter(Boolean)

    // Check prefixes first (most reliable)
    if (parts.length > 0) {
      const prefix = parts[0]
      if (FEMALE_PREFIXES.includes(prefix)) return 'female'
      if (MALE_PREFIXES.includes(prefix)) return 'male'
    }

    // Check first name (first part, or second part if first was a title)
    for (const part of parts) {
      if (FEMALE_NAMES.has(part)) return 'female'
      if (MALE_NAMES.has(part)) return 'male'
    }

    return null
  }

  /**
   * Speak French text, optionally selecting voice gender based on speaker name.
   * @param {string} text - The text to speak.
   * @param {object} options
   * @param {number} options.rate - Speech rate (default 0.85).
   * @param {string} options.speaker - Speaker name for gender detection (e.g. "Léa", "M. Merle").
   */
  function speak(text, { rate = 0.85, speaker = null } = {}) {
    if (!isSupported.value || !text) return

    speechSynthesis.cancel()
    if (!voicesLoaded) loadVoices()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'fr-FR'
    utterance.rate = rate

    // Select voice based on speaker gender
    const gender = guessGender(speaker)
    if (gender === 'female' && femaleVoice) {
      utterance.voice = femaleVoice
    } else if (gender === 'male' && maleVoice) {
      utterance.voice = maleVoice
    } else if (fallbackVoice) {
      utterance.voice = fallbackVoice
    }

    utterance.onstart = () => { isSpeaking.value = true }
    utterance.onend = () => { isSpeaking.value = false }
    utterance.onerror = () => { isSpeaking.value = false }

    speechSynthesis.speak(utterance)
  }

  function stop() {
    if (!isSupported.value) return
    speechSynthesis.cancel()
    isSpeaking.value = false
  }

  onBeforeUnmount(() => {
    stop()
    if (isSupported.value) {
      speechSynthesis.removeEventListener('voiceschanged', loadVoices)
    }
  })

  return { speak, stop, isSpeaking, isSupported }
}

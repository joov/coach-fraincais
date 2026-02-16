import { ref } from 'vue'

/**
 * Composable for audio recording via the MediaRecorder API.
 * Records in audio/webm;codecs=opus format.
 */
export function useRecorder() {
  const isRecording = ref(false)
  const audioBlob = ref(null)
  const error = ref(null)

  let mediaRecorder = null
  let chunks = []

  /**
   * Start recording from the microphone.
   * Requests permission if not already granted.
   */
  async function startRecording() {
    error.value = null
    audioBlob.value = null
    chunks = []

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

      const mimeType = 'audio/webm;codecs=opus'
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        throw new Error(`MIME type ${mimeType} is not supported in this browser.`)
      }

      mediaRecorder = new MediaRecorder(stream, { mimeType })

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data)
        }
      }

      mediaRecorder.onerror = (e) => {
        error.value = e.error?.message || 'Recording error'
        isRecording.value = false
      }

      mediaRecorder.start()
      isRecording.value = true
    } catch (err) {
      error.value = err.message || 'Could not start recording'
      isRecording.value = false
    }
  }

  /**
   * Stop the current recording.
   * @returns {Promise<Blob>} The recorded audio as a Blob.
   */
  function stopRecording() {
    return new Promise((resolve, reject) => {
      if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        const msg = 'No active recording to stop'
        error.value = msg
        reject(new Error(msg))
        return
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm;codecs=opus' })
        audioBlob.value = blob
        chunks = []
        isRecording.value = false

        // Release the microphone
        mediaRecorder.stream.getTracks().forEach((track) => track.stop())
        mediaRecorder = null

        resolve(blob)
      }

      mediaRecorder.stop()
    })
  }

  return { startRecording, stopRecording, isRecording, audioBlob, error }
}

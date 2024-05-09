    document.addEventListener('DOMContentLoaded', async () => {
        const recordedChunks = [];
        const stream = await navigator.mediaDevices.getUserMedia({audio: true})
        const mediaRecorder = new MediaRecorder(stream)
        const handleStartRecording = () => {
            document.querySelector('.start-recording').classList.add('hidden')
            document.querySelector('.recording').classList.remove('hidden')
            startRecording()
        }

        // Stop Recording handler
        const handleStopRecording = () => {
            document.querySelector('.recording').classList.add('hidden')
            document.querySelector('.start-recording').classList.remove('hidden')
            stopRecording()
        }

        const startRecording = async () => {
            if (mediaRecorder.state === 'inactive') {
                recordedChunks.length = 0
                mediaRecorder.start()
            }
        }

        const stopRecording = async () => {
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop()
            }
        }

        // MediaRecorder handler for available data
        // It adds received data to chunks, so it can be processed latter
        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) recordedChunks.push(event.data)
        }

        // MediaRecorder handler for stop action
        // It transforms audio chunks into blob and sends it /process-audio endpoint
        // If the response is ok then it plays response sent by LLM
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(recordedChunks, {type: 'audio/webm'})
            const formData = new FormData();
            formData.append('audio', audioBlob)

            const resposne = await fetch('/process-audio', {
                method: 'POST',
                body: formData
            })

            if (resposne.ok) {
                console.log('Audio uploaded successfully')
                const returnedBlob = await resposne.blob()
                const returnedUrl = URL.createObjectURL(returnedBlob)
                await new Audio(returnedUrl).play()
            }
        }

        // Add listeners for buttons click
        document.querySelector('.start-recording').addEventListener('click', handleStartRecording)
        document.querySelector('.recording').addEventListener('click', handleStopRecording)
    })
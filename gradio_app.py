import os
import gradio as gr

from brain_of_doctor import encode_image, analyze_image_with_query
from voice_of_patient import record_audio, transcribe_with_groq
from voice_of_doctor import text_to_speech_with_gtts

system_prompt="""You have to act as a professional doctor, I know you are not but this is for learning purposes. 
            What's in this image? Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also, always answer as if you are answering a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Do not respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away, please."""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="llama-3.2-90b-vision-preview"  # Ensure this matches `brain_of_doctor.py`
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # ✅ FIX: Use Google TTS instead of ElevenLabs
    voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3")

    return speech_to_text_output, doctor_response, "final.mp3"  # Match audio file

# Create the Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final.mp3")  # ✅ Match correct file
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)

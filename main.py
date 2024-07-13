import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import random
import textwrap
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips



def fit_text_to_box(draw, text, box_width, box_height, font_name, start_size=48, min_size=20):
    font_size = start_size
    font = ImageFont.truetype(font_name, font_size)
    lines = []
    
    while font_size >= min_size:
        lines = []
        line_height = font.getbbox('hg')[3] - font.getbbox('hg')[1]
        y = 0
        for word in text.split():
            if not lines:
                lines.append(word)
            else:
                line = f'{lines[-1]} {word}'
                bbox = font.getbbox(line)
                if bbox[2] <= box_width:
                    lines[-1] = line
                else:
                    lines.append(word)
            
            if (len(lines) * line_height) > box_height:
                break
        
        if (len(lines) * line_height) <= box_height:
            return font, lines
        
        font_size -= 1
        font = ImageFont.truetype(font_name, font_size)
    
    return font, lines

def create_video_from_random_image(folder_path, output_path, quote, duration=5):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if not image_files:
        print("No image files found in the specified folder.")
        return
    
    random_image = random.choice(image_files)
    image_path = os.path.join(folder_path, random_image)
    
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    # Define text box dimensions
    box_width = int(width * 0.9)
    box_height = int(height * 0.3)
    
    try:
        font, lines = fit_text_to_box(draw, quote, box_width, box_height, "arial.ttf")
    except IOError:
        font = ImageFont.load_default()
        lines = textwrap.wrap(quote, width=30)

    line_height = font.getbbox('hg')[3] - font.getbbox('hg')[1]
    total_text_height = len(lines) * line_height

    # Position text at the bottom of the image
    start_y = height - total_text_height - int(height * 0.25)  # 5% padding from bottom

    for line in lines:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2

        # Add shadow
        shadow_offset = 2
        for offset in range(shadow_offset, 0, -1):
            shadow_position = (x + offset, start_y + offset)
            draw.text(shadow_position, line, font=font, fill=(0, 0, 0, 128))

        # Add main text
        draw.text((x, start_y), line, font=font, fill=(255, 255, 255))

        start_y += line_height

    img_with_text = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    for _ in range(int(duration * 30)):
        video.write(img_with_text)

    video.release()
    print(f"Video created from image: {random_image}")




def convert_mp4_to_mov(mp4_path, mov_path, audio_path):
    # Load the video and audio clips
    video_clip = VideoFileClip(mp4_path)
    audio_clip = AudioFileClip(audio_path).set_duration(10)  # Set audio duration to 10 seconds

    # Ensure video duration is exactly 10 seconds
    if video_clip.duration < 10:
        # Loop the video if it's shorter than 10 seconds
        n_loops = int(np.ceil(10 / video_clip.duration))
        video_clip = concatenate_videoclips([video_clip] * n_loops).subclip(0, 10)
    else:
        # Trim the video if it's longer than 10 seconds
        video_clip = video_clip.subclip(0, 10)

    # Set the audio to the video clip
    final_clip = video_clip.set_audio(audio_clip)
    
    # Write the final clip to a file
    final_clip.write_videofile(mov_path, codec='libx264')
    print(f"Converted {mp4_path} to {mov_path} with audio")

# Example usage
folder_path = "Collections"
output_path = "output_video.mp4"


quotes = [
    "When you finally find a quiet spot to check your phone",
    "Waiting for your friends to come online like...",
    "When you're the first one to arrive at the meeting spot",
    "That moment when you realize you left the oven on at home",
    "When you're trying to enjoy nature but can't stop thinking about work",
    "Contemplating whether to order takeout for the third time this week",
    "When you're on vacation but remember all the emails waiting for you",
    "Trying to remember if you locked the front door",
    "When you're enjoying the view but also wondering what's for dinner",
    "That feeling when you're ready for adventure but also kind of want a nap",
    "When you find the perfect Instagram spot but your phone is at 1%",
    "Wondering if it's too late to cancel plans and stay in",
    "When you're enjoying solitude but also lowkey hoping someone texts you",
    "That moment of peace before remembering your to-do list",
    "When you're trying to be one with nature but can't stop thinking about Wi-Fi"
]
#
# quotes = [
#     "Sometimes the bravest thing is just getting out of bed.",
#     "Your anxiety lies to you. Your strength tells the truth.",
#     "It's okay to be a work in progress.",
#     "The voice in your head that says you can't do it is lying.",
#     "Healing isn't linear, but it's always possible.",
#     "You've survived 100% of your worst days. Keep going.",
#     "It's not about being fearless, it's about facing fears.",
#     "Your struggles are part of your story, not the end of it.",
#     "Sometimes, being alone is when you find yourself.",
#     "Small steps still move you forward.",
#     "You're allowed to outgrow who you used to be.",
#     "The hardest battles are fought within.",
#     "It's okay to not be okay, but it's not okay to give up.",
#     "Your worth isn't measured by your productivity.",
#     "Being different isn't a flaw, it's your superpower.",
#     "The mightiest dragon you'll ever slay lurks within your own heart.",
#     "Your inner demons are just challenges waiting to be overcome.",
#     "In the silence of solitude, your true strength speaks loudest.",
#     "Every step forward is a victory, no matter how small.",
#     "Your past doesn't define you, your resilience does.",
#     "The darkest nights produce the brightest stars within us.",
#     "Embracing your flaws is the first step to overcoming them.",
#     "Your journey is unique, don't compare your chapter 1 to someone else's chapter 20.",
#     "The strongest people are those who win battles we know nothing about.",
#     "Your potential is limitless, your fears are not."
# ]

# Randomly select a quote
quote = random.choice(quotes)

# quote = "The mightiest dragon you'll ever slay lurks within your own heart."
create_video_from_random_image(folder_path, output_path, quote)

mov_output_path = "output_video.mov"
audio_path = "audio.wav"
convert_mp4_to_mov(output_path, mov_output_path, audio_path)

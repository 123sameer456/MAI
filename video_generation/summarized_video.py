import random
import numpy as np
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips, CompositeVideoClip,
    vfx, afx
)

def create_summarized_video(video_path, output_path="summarized_video.mp4"):
    """
    Create a summarized video with various effects applied.
    
    Args:
        video_path (str): Path to the input video file
        output_path (str): Path for the output summarized video
    
    Returns:
        str: Path to the generated summarized video
    """
    
    # Load the video
    video = VideoFileClip(video_path)
    original_duration = video.duration
    
    # Calculate target duration (25% of original)
    target_duration = original_duration * 0.25
    
    # Calculate number of segments needed (10 seconds each)
    num_segments = int(target_duration // 10)
    if num_segments == 0:
        num_segments = 1
    
    # Ensure we have at least some segments
    segment_duration = min(10, target_duration / num_segments)
    
    print(f"Original duration: {original_duration:.2f}s")
    print(f"Target duration: {target_duration:.2f}s")
    print(f"Creating {num_segments} segments of {segment_duration:.2f}s each")
    
    # Generate random start times for segments, distributed across the video
    segments = []
    
    # Divide video into sections to ensure good distribution
    section_size = original_duration / (num_segments + 1)
    
    for i in range(num_segments):
        # Calculate the center of each section
        section_center = (i + 1) * section_size
        
        # Add some randomness around the center (±20% of section size)
        randomness = section_size * 0.4
        start_time = max(0, min(
            original_duration - segment_duration,
            section_center - segment_duration/2 + random.uniform(-randomness/2, randomness/2)
        ))
        
        end_time = min(start_time + segment_duration, original_duration)
        
        # Extract segment
        segment = video.subclip(start_time, end_time)
        
        # Apply random effects to each segment
        segment = apply_random_effects(segment, i)
        
        segments.append(segment)
        print(f"Segment {i+1}: {start_time:.2f}s - {end_time:.2f}s")
    
    # Concatenate all segments
    final_video = concatenate_videoclips(segments, method="compose")
    
    # Apply final fade in/out to the entire video
    final_video = final_video.fadein(1).fadeout(1)
    
    # Write the final video
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Clean up
    video.close()
    final_video.close()
    for segment in segments:
        segment.close()
    
    print(f"Summarized video saved as: {output_path}")
    return output_path

def apply_random_effects(clip, segment_index):
    """
    Apply random effects to a video segment.
    
    Args:
        clip: MoviePy VideoClip object
        segment_index: Index of the segment (for variety)
    
    Returns:
        VideoClip: Modified clip with effects applied
    """
    
    # List of possible speed multipliers
    speed_options = [1.0, 1.25, 1.5]
    
    # Randomly select speed
    speed = random.choice(speed_options)
    if speed != 1.0:
        clip = clip.fx(vfx.speedx, speed)
        print(f"  Applied {speed}x speed")
    
    # Apply rotation (random angle between -15 and 15 degrees)
    if random.random() < 0.4:  # 40% chance of rotation
        angle = random.uniform(-15, 15)
        clip = clip.fx(vfx.rotate, angle)
        print(f"  Applied {angle:.1f}° rotation")
    
    # Apply zoom effect
    if random.random() < 0.3:  # 30% chance of zoom
        zoom_factor = random.uniform(1.1, 1.3)
        clip = clip.fx(vfx.resize, zoom_factor)
        print(f"  Applied {zoom_factor:.2f}x zoom")
    
    # Apply black and white effect
    if random.random() < 0.2:  # 20% chance of B&W
        clip = clip.fx(vfx.blackwhite)
        print("  Applied black & white effect")
    
    # Apply mirror effect
    if random.random() < 0.15:  # 15% chance of mirror
        if random.choice([True, False]):
            clip = clip.fx(vfx.mirror_x)
            print("  Applied horizontal mirror")
        else:
            clip = clip.fx(vfx.mirror_y)
            print("  Applied vertical mirror")
    
    # Apply fade in/out to segment
    fade_duration = min(0.5, clip.duration / 4)
    clip = clip.fadein(fade_duration).fadeout(fade_duration)
    
    # Apply audio effects if clip has audio
    if clip.audio is not None:
        # Random volume adjustment
        volume_options = [0.3, 0.5, 0.8, 1.0, 1.2, 1.5]  # Low to high volume
        volume = random.choice(volume_options)
        clip = clip.fx(afx.volumex, volume)
        
        if volume <= 0.5:
            print(f"  Applied low volume ({volume}x)")
        elif volume >= 1.2:
            print(f"  Applied high volume ({volume}x)")
        else:
            print(f"  Applied normal volume ({volume}x)")
        
        # Occasionally apply audio fade
        if random.random() < 0.3:  # 30% chance
            audio_fade = min(0.3, clip.duration / 6)
            clip = clip.audio_fadein(audio_fade).audio_fadeout(audio_fade)
            print("  Applied audio fade in/out")
    
    return clip

def create_advanced_summarized_video(video_path, output_path="advanced_summary.mp4"):
    """
    Enhanced version with more sophisticated effects and transitions.
    """
    
    video = VideoFileClip(video_path)
    original_duration = video.duration
    target_duration = original_duration * 0.25
    
    # Create segments with overlap for smoother transitions
    num_segments = max(1, int(target_duration // 8))  # 8-second segments for more variety
    segment_duration = 8
    
    segments = []
    
    # Use different sampling strategies
    sampling_strategies = ['uniform', 'beginning_heavy', 'end_heavy', 'random']
    strategy = random.choice(sampling_strategies)
    
    print(f"Using {strategy} sampling strategy")
    
    start_times = generate_start_times(original_duration, num_segments, segment_duration, strategy)
    
    for i, start_time in enumerate(start_times):
        end_time = min(start_time + segment_duration, original_duration)
        segment = video.subclip(start_time, end_time)
        
        # Apply effects with more variety
        segment = apply_advanced_effects(segment, i, num_segments)
        
        segments.append(segment)
    
    # Create transitions between segments
    final_segments = []
    for i, segment in enumerate(segments):
        final_segments.append(segment)
        
        # Add transition effect (except for last segment)
        if i < len(segments) - 1 and random.random() < 0.3:
            # Create a short transition clip
            transition = create_transition_effect(segment, segments[i + 1])
            if transition:
                final_segments.append(transition)
    
    # Concatenate with crossfade
    final_video = concatenate_videoclips(final_segments, method="compose")
    
    # Apply final color correction
    if random.random() < 0.5:
        # Adjust gamma/contrast
        final_video = final_video.fx(vfx.gamma_corr, random.uniform(0.8, 1.2))
    
    final_video = final_video.fadein(1.5).fadeout(1.5)
    
    # Write with high quality settings
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        bitrate='8000k',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Cleanup
    video.close()
    final_video.close()
    for segment in segments:
        segment.close()
    
    return output_path

def generate_start_times(duration, num_segments, segment_duration, strategy):
    """Generate start times based on different sampling strategies."""
    
    if strategy == 'uniform':
        # Evenly distributed
        step = (duration - segment_duration) / (num_segments - 1) if num_segments > 1 else 0
        return [i * step for i in range(num_segments)]
    
    elif strategy == 'beginning_heavy':
        # More segments from the beginning
        times = []
        for i in range(num_segments):
            # Exponential decay
            progress = i / max(num_segments - 1, 1)
            start_time = (duration - segment_duration) * (progress ** 2)
            times.append(start_time)
        return times
    
    elif strategy == 'end_heavy':
        # More segments from the end
        times = []
        for i in range(num_segments):
            progress = i / max(num_segments - 1, 1)
            start_time = (duration - segment_duration) * (1 - (1 - progress) ** 2)
            times.append(start_time)
        return times
    
    else:  # random
        times = []
        for _ in range(num_segments):
            max_start = duration - segment_duration
            times.append(random.uniform(0, max_start))
        return sorted(times)

def apply_advanced_effects(clip, index, total_segments):
    """Apply more sophisticated effects."""
    
    # Progressive effects based on position in sequence
    position_ratio = index / max(total_segments - 1, 1)
    
    # Speed effects with more variation
    if random.random() < 0.7:  # Higher chance of speed change
        speed_curves = {
            'slow_start': [0.8, 1.0, 1.25, 1.5],
            'fast_start': [1.5, 1.25, 1.0, 0.8],
            'random': [1.0, 1.25, 1.5, 0.75, 2.0]
        }
        
        curve_type = random.choice(list(speed_curves.keys()))
        speeds = speed_curves[curve_type]
        speed = speeds[int(position_ratio * (len(speeds) - 1))]
        
        clip = clip.fx(vfx.speedx, speed)
        print(f"  Segment {index}: Applied {speed}x speed ({curve_type})")
    
    # More creative visual effects
    effect_chance = 0.6
    if random.random() < effect_chance:
        effects = [
            ('rotate', lambda c: c.fx(vfx.rotate, random.uniform(-20, 20))),
            ('zoom', lambda c: c.fx(vfx.resize, random.uniform(1.1, 1.4))),
            ('bw', lambda c: c.fx(vfx.blackwhite)),
            ('invert', lambda c: c.fx(vfx.invert_colors)),
            ('blur', lambda c: c.fx(vfx.blur, 1.5)),
            ('mirror_x', lambda c: c.fx(vfx.mirror_x)),
            ('mirror_y', lambda c: c.fx(vfx.mirror_y)),
        ]
        
        effect_name, effect_func = random.choice(effects)
        try:
            clip = effect_func(clip)
            print(f"  Segment {index}: Applied {effect_name} effect")
        except Exception as e:
            print(f"  Segment {index}: Failed to apply {effect_name}: {e}")
    
    # Audio effects
    if clip.audio is not None:
        # More dynamic volume changes
        volume_progression = {
            'crescendo': 0.3 + (position_ratio * 0.9),
            'diminuendo': 1.2 - (position_ratio * 0.9),
            'random': random.choice([0.2, 0.4, 0.6, 0.8, 1.0, 1.3, 1.6])
        }
        
        progression_type = random.choice(list(volume_progression.keys()))
        volume = volume_progression[progression_type]
        
        clip = clip.fx(afx.volumex, volume)
        print(f"  Segment {index}: Applied {progression_type} volume ({volume:.2f}x)")
    
    # Fade effects
    fade_duration = min(1.0, clip.duration / 3)
    clip = clip.fadein(fade_duration).fadeout(fade_duration)
    
    return clip

def create_transition_effect(clip1, clip2):
    """Create a transition effect between two clips."""
    try:
        transition_duration = 0.5
        if clip1.duration < transition_duration or clip2.duration < transition_duration:
            return None
        
        # Take last part of clip1 and first part of clip2
        end_clip = clip1.subclip(-transition_duration)
        start_clip = clip2.subclip(0, transition_duration)
        
        # Create crossfade effect
        end_clip = end_clip.fadeout(transition_duration)
        start_clip = start_clip.fadein(transition_duration)
        
        # Composite them
        transition = CompositeVideoClip([end_clip, start_clip.set_start(0)])
        return transition.subclip(0, transition_duration)
    
    except Exception as e:
        print(f"Failed to create transition: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Basic usage
    video_file = "v.mp4"  # Replace with your video path
    
    # Create basic summarized video
    output1 = create_summarized_video(video_file, "basic_summary.mp4")
    
    # Create advanced summarized video
    output2 = create_advanced_summarized_video(video_file, "advanced_summary.mp4")
    
    print(f"\nGenerated videos:")
    print(f"1. Basic summary: {output1}")
    print(f"2. Advanced summary: {output2}")
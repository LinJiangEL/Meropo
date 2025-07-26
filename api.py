# ------------------
#       Meropo
# ------------------
import os
import dotenv
import base64
from openai import OpenAI
from gradio_client import Client, handle_file
from typing import Literal, Optional, Union, Tuple
dotenv.load_dotenv('.env')


def get_desktop_path():
    try:
        if os.name == 'nt':
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return os.getcwd()
    except Exception:
        return os.getcwd()


class MusicAPI:
    def __init__(self, api_url: str = "https://d07261654-acestep10-3024-syc5g9dc-7865.550c.cloud"):
        """
        Initialize the MusicAPI client.

        Args:
            api_url: The base URL of the API endpoint
        """
        self.client = Client(api_url)

    def toggle_ref_audio_visibilitity(self, is_checked=False) -> tuple[str, float]:
        """
        :param is_checked: The input value that is provided in the "Preset" Dropdown component.
        :return: (filepath, float) -> ("Reference Audio (for Audio2Audio)", "Refer audio strength")
        """
        return self.client.predict(
            is_checked=is_checked,
            api_name="/toggle_ref_audio_visibility"
        )

    def update_tags_from_preset(self, preset_name: Literal[
        'Custom', 'Modern Pop', 'Rock', 'Hip Hop', 'Country', 'EDM', 'Reggae', 'Classical', 'Jazz', 'Metal', 'R&B'] = "Custom") -> str:
        """
        :param preset_name: The input value that is provided in the "Preset" Dropdown component.
        :return: The output value that appears in the "Tags" Textbox component.
        """
        return self.client.predict(
            preset_name=preset_name,
            api_name="/update_tags_from_preset"
        )

    def retake_process_func(self, json_data, retake_variance, retake_seeds):
        """
        :param json_data: The input value that is provided in the "Text2Music Parameters" Json component.
        :param retake_variance: The input value that is provided in the "variance" Slider component.
        :param retake_seeds:The input value that is provided in the "retake seeds (default None)" Textbox component.
        :return: (filepath, str | float | bool | list | dict) -> ("Retake Generated Audio 1", "Retake Parameters")
        """
        return self.client.predict(
            json_data={"foo": "bar"},
            retake_variance=0.2,
            retake_seeds="Hello!!",
            api_name="/retake_process_func"
        )

    def lambda_func(self, x: Literal['text2music', 'last_repaint', 'upload'] = "text2music") -> str:
        """
        Lambda function for repaint source selection.

        Args:
            x: Repaint source selection

        Returns:
            str: Path to the upload audio file
        """
        return self.client.predict(
            x=x,
            api_name="/lambda"
        )

    def repaint_process_func(
            self,
            text2music_json_data: Union[str, float, bool, list, dict],
            repaint_json_data: Union[str, float, bool, list, dict],
            retake_variance: float = 0.2,
            retake_seeds: str = "Hello!!",
            repaint_start: float = 0,
            repaint_end: float = 30,
            repaint_source: Literal['text2music', 'last_repaint', 'upload'] = "text2music",
            repaint_source_audio_upload: str = None,
            prompt: str = "funk, pop, soul, rock, melodic, guitar, drums, bass, keyboard, percussion, 105 BPM, energetic, upbeat, groovy, vibrant, dynamic",
            lyrics: str = "[verse]\nNeon lights they flicker bright\nCity hums in dead of night\nRhythms pulse through concrete veins\nLost in echoes of refrains\n\n[verse]\nBassline groovin' in my chest\nHeartbeats match the city's zest\nElectric whispers fill the air\nSynthesized dreams everywhere\n\n[chorus]\nTurn it up and let it flow\nFeel the fire let it grow\nIn this rhythm we belong\nHear the night sing out our song\n\n[verse]\nGuitar strings they start to weep\nWake the soul from silent sleep\nEvery note a story told\nIn this night we're bold and gold\n\n[bridge]\nVoices blend in harmony\nLost in pure cacophony\nTimeless echoes timeless cries\nSoulful shouts beneath the skies\n\n[verse]\nKeyboard dances on the keys\nMelodies on evening breeze\nCatch the tune and hold it tight\nIn this moment we take flight",
            infer_step: float = 60,
            guidance_scale: float = 15,
            scheduler_type: Literal['euler', 'heun', 'pingpong'] = "euler",
            cfg_type: Literal['cfg', 'apg', 'cfg_star'] = "apg",
            omega_scale: float = 10,
            manual_seeds: str = "Hello!!",
            guidance_interval: float = 0.5,
            guidance_interval_decay: float = 0,
            min_guidance_scale: float = 3,
            use_erg_tag: bool = True,
            use_erg_lyric: bool = False,
            use_erg_diffusion: bool = True,
            oss_steps: str = "Hello!!",
            guidance_scale_text: float = 0,
            guidance_scale_lyric: float = 0
    ) -> Tuple[str, Union[str, float, bool, list, dict]]:
        """
        Process audio repainting.

        Args:
            text2music_json_data: Text2Music Parameters in JSON format
            repaint_json_data: Repaint Parameters in JSON format
            retake_variance: Variance value for retake
            retake_seeds: Seeds for retake process
            repaint_start: Start time for repaint
            repaint_end: End time for repaint
            repaint_source: Source for repaint
            repaint_source_audio_upload: Path to upload audio file
            prompt: Tags for the music
            lyrics: Lyrics for the music
            infer_step: Number of inference steps
            guidance_scale: Guidance scale value
            scheduler_type: Type of scheduler to use
            cfg_type: Type of CFG to use
            omega_scale: Granularity scale value
            manual_seeds: Manual seeds for generation
            guidance_interval: Guidance interval value
            guidance_interval_decay: Guidance interval decay value
            min_guidance_scale: Minimum guidance scale value
            use_erg_tag: Whether to use ERG for tag
            use_erg_lyric: Whether to use ERG for lyric
            use_erg_diffusion: Whether to use ERG for diffusion
            oss_steps: OSS steps value
            guidance_scale_text: Guidance scale for text
            guidance_scale_lyric: Guidance scale for lyrics

        Returns:
            Tuple containing:
                - filepath: Path to the repainted audio file
                - JSON data of repaint parameters
        """
        if repaint_source_audio_upload:
            repaint_source_audio_upload = handle_file(repaint_source_audio_upload)

        return self.client.predict(
            text2music_json_data=text2music_json_data,
            repaint_json_data=repaint_json_data,
            retake_variance=retake_variance,
            retake_seeds=retake_seeds,
            repaint_start=repaint_start,
            repaint_end=repaint_end,
            repaint_source=repaint_source,
            repaint_source_audio_upload=repaint_source_audio_upload,
            prompt=prompt,
            lyrics=lyrics,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            scheduler_type=scheduler_type,
            cfg_type=cfg_type,
            omega_scale=omega_scale,
            manual_seeds=manual_seeds,
            guidance_interval=guidance_interval,
            guidance_interval_decay=guidance_interval_decay,
            min_guidance_scale=min_guidance_scale,
            use_erg_tag=use_erg_tag,
            use_erg_lyric=use_erg_lyric,
            use_erg_diffusion=use_erg_diffusion,
            oss_steps=oss_steps,
            guidance_scale_text=guidance_scale_text,
            guidance_scale_lyric=guidance_scale_lyric,
            api_name="/repaint_process_func"
        )

    def edit_type_change_func(self, edit_type: Literal['only_lyrics', 'remix'] = "only_lyrics") -> Tuple[float, float]:
        """
        Change edit type and get corresponding min/max values.

        Args:
            edit_type: Type of edit to perform

        Returns:
            Tuple containing:
                - float: edit_n_min value
                - float: edit_n_max value
        """
        return self.client.predict(
            edit_type=edit_type,
            api_name="/edit_type_change_func"
        )

    def lambda_func_1(self, x: Literal['text2music', 'last_edit', 'upload'] = "text2music") -> str:
        """
        Lambda function for edit source selection.

        Args:
            x: Edit source selection

        Returns:
            str: Path to the upload audio file
        """
        return self.client.predict(
            x=x,
            api_name="/lambda_1"
        )

    def edit_process_func(
            self,
            text2music_json_data: Union[str, float, bool, list, dict],
            edit_input_params_json: Union[str, float, bool, list, dict],
            edit_source: Literal['text2music', 'last_edit', 'upload'] = "text2music",
            edit_source_audio_upload: str = None,
            prompt: str = "funk, pop, soul, rock, melodic, guitar, drums, bass, keyboard, percussion, 105 BPM, energetic, upbeat, groovy, vibrant, dynamic",
            lyrics: str = "[verse]\nNeon lights they flicker bright\nCity hums in dead of night\nRhythms pulse through concrete veins\nLost in echoes of refrains\n\n[verse]\nBassline groovin' in my chest\nHeartbeats match the city's zest\nElectric whispers fill the air\nSynthesized dreams everywhere\n\n[chorus]\nTurn it up and let it flow\nFeel the fire let it grow\nIn this rhythm we belong\nHear the night sing out our song\n\n[verse]\nGuitar strings they start to weep\nWake the soul from silent sleep\nEvery note a story told\nIn this night we're bold and gold\n\n[bridge]\nVoices blend in harmony\nLost in pure cacophony\nTimeless echoes timeless cries\nSoulful shouts beneath the skies\n\n[verse]\nKeyboard dances on the keys\nMelodies on evening breeze\nCatch the tune and hold it tight\nIn this moment we take flight",
            edit_prompt: str = "Hello!!",
            edit_lyrics: str = "Hello!!",
            edit_n_min: float = 0.6,
            edit_n_max: float = 1,
            infer_step: float = 60,
            guidance_scale: float = 15,
            scheduler_type: Literal['euler', 'heun', 'pingpong'] = "euler",
            cfg_type: Literal['cfg', 'apg', 'cfg_star'] = "apg",
            omega_scale: float = 10,
            manual_seeds: str = "Hello!!",
            guidance_interval: float = 0.5,
            guidance_interval_decay: float = 0,
            min_guidance_scale: float = 3,
            use_erg_tag: bool = True,
            use_erg_lyric: bool = False,
            use_erg_diffusion: bool = True,
            oss_steps: str = "Hello!!",
            guidance_scale_text: float = 0,
            guidance_scale_lyric: float = 0,
            retake_seeds: str = "Hello!!"
    ) -> Tuple[str, Union[str, float, bool, list, dict]]:
        """
        Process audio editing.

        Args:
            text2music_json_data: Text2Music Parameters in JSON format
            edit_input_params_json: Edit Parameters in JSON format
            edit_source: Source for edit
            edit_source_audio_upload: Path to upload audio file
            prompt: Tags for the music
            lyrics: Lyrics for the music
            edit_prompt: Edited tags
            edit_lyrics: Edited lyrics
            edit_n_min: Minimum edit value
            edit_n_max: Maximum edit value
            infer_step: Number of inference steps
            guidance_scale: Guidance scale value
            scheduler_type: Type of scheduler to use
            cfg_type: Type of CFG to use
            omega_scale: Granularity scale value
            manual_seeds: Manual seeds for generation
            guidance_interval: Guidance interval value
            guidance_interval_decay: Guidance interval decay value
            min_guidance_scale: Minimum guidance scale value
            use_erg_tag: Whether to use ERG for tag
            use_erg_lyric: Whether to use ERG for lyric
            use_erg_diffusion: Whether to use ERG for diffusion
            oss_steps: OSS steps value
            guidance_scale_text: Guidance scale for text
            guidance_scale_lyric: Guidance scale for lyrics
            retake_seeds: Seeds for retake process

        Returns:
            Tuple containing:
                - filepath: Path to the edited audio file
                - JSON data of edit parameters
        """
        if edit_source_audio_upload:
            edit_source_audio_upload = handle_file(edit_source_audio_upload)

        return self.client.predict(
            text2music_json_data=text2music_json_data,
            edit_input_params_json=edit_input_params_json,
            edit_source=edit_source,
            edit_source_audio_upload=edit_source_audio_upload,
            prompt=prompt,
            lyrics=lyrics,
            edit_prompt=edit_prompt,
            edit_lyrics=edit_lyrics,
            edit_n_min=edit_n_min,
            edit_n_max=edit_n_max,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            scheduler_type=scheduler_type,
            cfg_type=cfg_type,
            omega_scale=omega_scale,
            manual_seeds=manual_seeds,
            guidance_interval=guidance_interval,
            guidance_interval_decay=guidance_interval_decay,
            min_guidance_scale=min_guidance_scale,
            use_erg_tag=use_erg_tag,
            use_erg_lyric=use_erg_lyric,
            use_erg_diffusion=use_erg_diffusion,
            oss_steps=oss_steps,
            guidance_scale_text=guidance_scale_text,
            guidance_scale_lyric=guidance_scale_lyric,
            retake_seeds=retake_seeds,
            api_name="/edit_process_func"
        )

    def lambda_func_2(self, x: Literal['text2music', 'last_extend', 'upload'] = "text2music") -> str:
        """
        Lambda function for extend source selection.

        Args:
            x: Extend source selection

        Returns:
            str: Path to the upload audio file
        """
        return self.client.predict(
            x=x,
            api_name="/lambda_2"
        )

    def extend_process_func(
            self,
            text2music_json_data: Union[str, float, bool, list, dict],
            extend_input_params_json: Union[str, float, bool, list, dict],
            extend_seeds: str = "Hello!!",
            left_extend_length: float = 0,
            right_extend_length: float = 30,
            extend_source: Literal['text2music', 'last_extend', 'upload'] = "text2music",
            extend_source_audio_upload: str = None,
            prompt: str = "funk, pop, soul, rock, melodic, guitar, drums, bass, keyboard, percussion, 105 BPM, energetic, upbeat, groovy, vibrant, dynamic",
            lyrics: str = "[verse]\nNeon lights they flicker bright\nCity hums in dead of night\nRhythms pulse through concrete veins\nLost in echoes of refrains\n\n[verse]\nBassline groovin' in my chest\nHeartbeats match the city's zest\nElectric whispers fill the air\nSynthesized dreams everywhere\n\n[chorus]\nTurn it up and let it flow\nFeel the fire let it grow\nIn this rhythm we belong\nHear the night sing out our song\n\n[verse]\nGuitar strings they start to weep\nWake the soul from silent sleep\nEvery note a story told\nIn this night we're bold and gold\n\n[bridge]\nVoices blend in harmony\nLost in pure cacophony\nTimeless echoes timeless cries\nSoulful shouts beneath the skies\n\n[verse]\nKeyboard dances on the keys\nMelodies on evening breeze\nCatch the tune and hold it tight\nIn this moment we take flight",
            infer_step: float = 60,
            guidance_scale: float = 15,
            scheduler_type: Literal['euler', 'heun', 'pingpong'] = "euler",
            cfg_type: Literal['cfg', 'apg', 'cfg_star'] = "apg",
            omega_scale: float = 10,
            manual_seeds: str = "Hello!!",
            guidance_interval: float = 0.5,
            guidance_interval_decay: float = 0,
            min_guidance_scale: float = 3,
            use_erg_tag: bool = True,
            use_erg_lyric: bool = False,
            use_erg_diffusion: bool = True,
            oss_steps: str = "Hello!!",
            guidance_scale_text: float = 0,
            guidance_scale_lyric: float = 0
    ) -> Tuple[str, Union[str, float, bool, list, dict]]:
        """
        Process audio extension.

        Args:
            text2music_json_data: Text2Music Parameters in JSON format
            extend_input_params_json: Extend Parameters in JSON format
            extend_seeds: Seeds for extend process
            left_extend_length: Length to extend on left
            right_extend_length: Length to extend on right
            extend_source: Source for extend
            extend_source_audio_upload: Path to upload audio file
            prompt: Tags for the music
            lyrics: Lyrics for the music
            infer_step: Number of inference steps
            guidance_scale: Guidance scale value
            scheduler_type: Type of scheduler to use
            cfg_type: Type of CFG to use
            omega_scale: Granularity scale value
            manual_seeds: Manual seeds for generation
            guidance_interval: Guidance interval value
            guidance_interval_decay: Guidance interval decay value
            min_guidance_scale: Minimum guidance scale value
            use_erg_tag: Whether to use ERG for tag
            use_erg_lyric: Whether to use ERG for lyric
            use_erg_diffusion: Whether to use ERG for diffusion
            oss_steps: OSS steps value
            guidance_scale_text: Guidance scale for text
            guidance_scale_lyric: Guidance scale for lyrics

        Returns:
            Tuple containing:
                - filepath: Path to the extended audio file
                - JSON data of extend parameters
        """
        if extend_source_audio_upload:
            extend_source_audio_upload = handle_file(extend_source_audio_upload)

        return self.client.predict(
            text2music_json_data=text2music_json_data,
            extend_input_params_json=extend_input_params_json,
            extend_seeds=extend_seeds,
            left_extend_length=left_extend_length,
            right_extend_length=right_extend_length,
            extend_source=extend_source,
            extend_source_audio_upload=extend_source_audio_upload,
            prompt=prompt,
            lyrics=lyrics,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            scheduler_type=scheduler_type,
            cfg_type=cfg_type,
            omega_scale=omega_scale,
            manual_seeds=manual_seeds,
            guidance_interval=guidance_interval,
            guidance_interval_decay=guidance_interval_decay,
            min_guidance_scale=min_guidance_scale,
            use_erg_tag=use_erg_tag,
            use_erg_lyric=use_erg_lyric,
            use_erg_diffusion=use_erg_diffusion,
            oss_steps=oss_steps,
            guidance_scale_text=guidance_scale_text,
            guidance_scale_lyric=guidance_scale_lyric,
            api_name="/extend_process_func"
        )

    def sample_data(self, lora_name_or_path_: Literal['ACE-Step/ACE-Step-v1-chinese-rap-LoRA', 'none'] = "none") -> \
            Tuple[float, str, str, float, float, Literal['euler', 'heun', 'pingpong'], Literal[
                'cfg', 'apg', 'cfg_star'], float, str, float, float, float, bool, bool, bool, str, float, float, bool, float, str]:
        """
        Get sample data based on LoRA selection.

        Args:
            lora_name_or_path_: LoRA name or path to use

        Returns:
            Tuple containing various parameters for music generation
        """
        return self.client.predict(
            lora_name_or_path_=lora_name_or_path_,
            api_name="/sample_data"
        )

    def load_data(self, json_file: str) -> Tuple[
        float, str, str, float, float, Literal['euler', 'heun', 'pingpong'], Literal[
            'cfg', 'apg', 'cfg_star'], float, str, float, float, float, bool, bool, bool, str, float, float, bool, float, str]:
        """
        Load data from a previously generated JSON file.

        Args:
            json_file: Path to the JSON file to load

        Returns:
            Tuple containing various parameters for music generation
        """
        return self.client.predict(
            json_file=json_file,
            api_name="/load_data"
        )

    def generate_music(
            self,
            format: Literal['mp3', 'ogg', 'flac', 'wav'] = "wav",
            audio_duration: float = -1,
            prompt: str = "funk, pop, soul, rock, melodic, guitar, drums, bass, keyboard, percussion, 105 BPM, energetic, upbeat, groovy, vibrant, dynamic",
            lyrics: str = "[verse]\nNeon lights they flicker bright\nCity hums in dead of night\nRhythms pulse through concrete veins\nLost in echoes of refrains\n\n[verse]\nBassline groovin' in my chest\nHeartbeats match the city's zest\nElectric whispers fill the air\nSynthesized dreams everywhere\n\n[chorus]\nTurn it up and let it flow\nFeel the fire let it grow\nIn this rhythm we belong\nHear the night sing out our song\n\n[verse]\nGuitar strings they start to weep\nWake the soul from silent sleep\nEvery note a story told\nIn this night we're bold and gold\n\n[bridge]\nVoices blend in harmony\nLost in pure cacophony\nTimeless echoes timeless cries\nSoulful shouts beneath the skies\n\n[verse]\nKeyboard dances on the keys\nMelodies on evening breeze\nCatch the tune and hold it tight\nIn this moment we take flight",
            infer_step: float = 60,
            guidance_scale: float = 15,
            scheduler_type: Literal['euler', 'heun', 'pingpong'] = "euler",
            cfg_type: Literal['cfg', 'apg', 'cfg_star'] = "apg",
            omega_scale: float = 10,
            manual_seeds: Optional[str] = None,
            guidance_interval: float = 0.5,
            guidance_interval_decay: float = 0,
            min_guidance_scale: float = 3,
            use_erg_tag: bool = True,
            use_erg_lyric: bool = False,
            use_erg_diffusion: bool = True,
            oss_steps: Optional[str] = None,
            guidance_scale_text: float = 0,
            guidance_scale_lyric: float = 0,
            audio2audio_enable: bool = False,
            ref_audio_strength: float = 0.5,
            ref_audio_input: Optional[str] = None,
            lora_name_or_path: Literal['ACE-Step/ACE-Step-v1-chinese-rap-LoRA', 'none'] = "none",
            lora_weight: float = 1
    ) -> Tuple[str, Union[str, float, bool, list, dict]]:
        """
        Generate music from text parameters.

        Args:
            format: Output audio format
            audio_duration: Duration of audio to generate
            prompt: Tags for the music
            lyrics: Lyrics for the music
            infer_step: Number of inference steps
            guidance_scale: Guidance scale value
            scheduler_type: Type of scheduler to use
            cfg_type: Type of CFG to use
            omega_scale: Granularity scale value
            manual_seeds: Manual seeds for generation
            guidance_interval: Guidance interval value
            guidance_interval_decay: Guidance interval decay value
            min_guidance_scale: Minimum guidance scale value
            use_erg_tag: Whether to use ERG for tag
            use_erg_lyric: Whether to use ERG for lyric
            use_erg_diffusion: Whether to use ERG for diffusion
            oss_steps: OSS steps value
            guidance_scale_text: Guidance scale for text
            guidance_scale_lyric: Guidance scale for lyrics
            audio2audio_enable: Whether to enable audio2audio
            ref_audio_strength: Reference audio strength
            ref_audio_input: Path to reference audio file
            lora_name_or_path: LoRA name or path to use
            lora_weight: Weight for LoRA

        Returns:
            Tuple containing:
                - filepath: Path to the generated audio file
                - JSON data of generation parameters
        """
        if ref_audio_input:
            ref_audio_input = handle_file(ref_audio_input)

        return self.client.predict(
            format=format,
            audio_duration=audio_duration,
            prompt=prompt,
            lyrics=lyrics,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            scheduler_type=scheduler_type,
            cfg_type=cfg_type,
            omega_scale=omega_scale,
            manual_seeds=manual_seeds,
            guidance_interval=guidance_interval,
            guidance_interval_decay=guidance_interval_decay,
            min_guidance_scale=min_guidance_scale,
            use_erg_tag=use_erg_tag,
            use_erg_lyric=use_erg_lyric,
            use_erg_diffusion=use_erg_diffusion,
            oss_steps=oss_steps,
            guidance_scale_text=guidance_scale_text,
            guidance_scale_lyric=guidance_scale_lyric,
            audio2audio_enable=audio2audio_enable,
            ref_audio_strength=ref_audio_strength,
            ref_audio_input=ref_audio_input,
            lora_name_or_path=lora_name_or_path,
            lora_weight=lora_weight,
            api_name="/__call__"
        )


class AI:
    def __init__(self):
        self.client = OpenAI(
            api_key=f"{os.getenv('KIMI_APIKEY')}",
            base_url="https://api.moonshot.cn/v1",
        )
        self.history = [
            {"role": "system",
             "content": "你是一个音乐鉴赏家，你擅长中文和英文的对话。擅长从古至今任何旋律的鉴赏，你会为用户提供安全，有帮助，准确的回答。"
                        "同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色，暴力等问题的回答。"
             }
        ]

    def chat(self, query, history=None):
        if history is None:
            history = []
        history.append({
            "role": "user",
            "content": query
        })
        completion = self.client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=history,
            temperature=0.6,
        )
        result = completion.choices[0].message.content
        history.append({
            "role": "assistant",
            "content": result
        })
        return result

    def analyze_audio(self, audio_file_path: str, analysis_prompt: str = None) -> str:
        """
        使用Kimi AI分析音频文件
        
        Args:
            audio_file_path: 音频文件路径
            analysis_prompt: 分析提示词，如果为None则使用默认提示
            
        Returns:
            str: AI分析结果
        """
        try:
            if not os.path.exists(audio_file_path):
                return f"错误：音频文件不存在 - {audio_file_path}"

            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            file_extension = os.path.splitext(audio_file_path)[1].lower()

            mime_types = {
                '.wav': 'audio/wav',
                '.mp3': 'audio/mpeg',
                '.ogg': 'audio/ogg',
                '.flac': 'audio/flac'
            }
            mime_type = mime_types.get(file_extension, 'audio/wav')

            # 构建分析提示
            if analysis_prompt is None:
                analysis_prompt = """请对这个音频文件进行专业的音乐鉴赏分析，包括但不限于：
1. 音乐风格和流派识别
2. 节奏、节拍和速度分析
3. 旋律和和声特点
4. 乐器编配和音色评价
5. 整体音乐表现力和情感表达
6. 技术制作质量评估
7. 与类似风格音乐的对比
8. 改进建议（如果有的话）

请用专业但易懂的语言进行分析，并给出具体的评价和建议。"""

            # 构建消息内容
            message_content = f"""
{analysis_prompt}

音频文件信息：
- 文件名：{os.path.basename(audio_file_path)}
- 文件大小：{len(audio_data)} 字节
- 文件格式：{file_extension}

请基于以上信息对音频进行专业分析。
"""

            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的音乐鉴赏家，擅长分析各种类型的音乐作品。请根据提供的音频文件进行详细分析。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message_content
                        },
                        {
                            "type": "audio",
                            "audio": {
                                "data": audio_base64,
                                "mime_type": mime_type
                            }
                        }
                    ]
                }
            ]

            completion = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=messages,
                temperature=0.7,
            )

            result = completion.choices[0].message.content
            return result

        except Exception as e:
            return f"音频分析过程中出现错误：{str(e)}"

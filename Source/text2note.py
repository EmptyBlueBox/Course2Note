import os
from typing import List
from openai import OpenAI
import time

note_system_prompt = """您是一名计算机专业的笔记助手，能够根据课程材料帮助大学计算机学生创建结构良好、内容全面的笔记。"""
note_prompt = """请根据课程材料创建全面且结构良好的笔记，使用 markdown 格式编写笔记，包括适当的标题、项目符号和重点标记。
                
                内容要求：
                1. 总结出清晰的格式和逻辑结构, 但是不要遗漏关键信息!!!
                2. 突出关键概念和定义, 比如`进程表`, `页表`, `TLB` 等.
                4. 需要改正课程讲稿中的识别错误, 比如将读音 `cache` 识别为 `开始` 是识别错误, 需要改正为 `cache`
                
                格式要求：
                1. 只使用第二级及以下的标题，不要使用大标题，比如 `# 操作系统课程笔记` 是错误的，应该不用这样的表述
                2. 只使用无标号标题，比如 `## 2.存储体系` 是错误的，应该是 `## 存储体系`
                """

cleaner_system_prompt = """你是一位擅长整理文字的工作人员，能够将混乱口语化的语音识别文稿整理成书面化的文稿。"""
cleaner_prompt = """请你将混乱口语化的语音识别文稿整理成书面化的文稿, 将逻辑理顺, 越详细越好

                    内容要求：
                    1. 不要遗漏教授说的**任何**信息, 越细节越详细越好, 所有例子都要保留, **不要做任何形式的总结**!!!
                    2. 需要改正不规范的用语和模糊的音节, 比如将读音 `cache` 识别为 `开始` 是识别错误, 需要改正为 `cache`
                    3. 在教授说看课件的时候使用 `**[参考课件]**` 来表示
                    
                    格式要求：
                    1. 不使用 markdown 格式和加粗下划线等记号
                    2. 在适当的地方分段
                    3. 不要输出除了标题和内容之外的任何其他内容, 比如不要输出 `课程主题为操作系统的基本概念和流程。以下是整理后的书面化课程笔记：` 这样的提示词
                    """

system_prompt = {
    "note": note_system_prompt,
    "cleaner": cleaner_system_prompt,
}

job_prompt = {
    "note": note_prompt,
    "cleaner": cleaner_prompt,
}


class NoteGenerator:
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize OpenAI API client.

        Args:
            api_key (str): OpenAI API key
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def _chunk_text(self, text: str, max_tokens: int = 50_000) -> List[str]:
        """
        Split text into chunks that fit within token limits.

        Args:
            text (str): Text to split
            max_tokens (int): Maximum tokens per chunk, the CONTEXT WINDOW for gpt-4o is 128k, so we set max_tokens to 80k

        Returns:
            list: List of text chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            # Approximate token count (words / 0.75)
            word_tokens = len(word) // 3 + 1

            if current_length + word_tokens > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_tokens
            else:
                current_chunk.append(word)
                current_length += word_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def query_note(self, transcript: str, style: str, model: str) -> str:
        """
        Generate notes for a single section using OpenAI API.

        Args:
            transcript (str): Audio transcript text
            style (str): Style of the notes, either "note" or "cleaner"

        Returns:
            str: Generated notes
        """
        try:
            notes = []
            transcript_chunks = self._chunk_text(text=transcript)

            for transcript_chunk in transcript_chunks:
                # Prepare prompt
                prompt = f"""
                {job_prompt[style]}
                
                **以下是课程讲稿：**
                {transcript_chunk}
                """

                # Split content into chunks if needed
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt[style]},
                        {"role": "user", "content": prompt},
                    ],
                    model=model,
                )

                notes.append(response.choices[0].message.content)

            return "\n\n".join(notes)

        except Exception as e:
            print(f"Error generating notes: {str(e)}")
            return ""


def generate_course_notes(
    transcript_dir: str,
    note_dir: str,
    base_url: str,
    api_key: str,
    model: str = "gpt-4o-mini",
    course_name: str = "OS",
    style: str = "cleaner",
) -> None:
    """
    Generate comprehensive notes for an entire course.

    Args:
        transcript_dir (str): Directory containing the transcripts
        note_dir (str): Directory to save the generated notes
        base_url (str): OpenAI API base URL
        api_key (str): OpenAI API key
        model (str): OpenAI model name
        course_name (str): Name of the course
        style (str): Style of the notes, either "note" or "cleaner"
    """
    try:
        generator = NoteGenerator(base_url=base_url, api_key=api_key)

        # Create output directory
        os.makedirs(note_dir, exist_ok=True)

        for section_name in os.listdir(transcript_dir):
            transcript_file_path = os.path.join(transcript_dir, section_name)
            section_name_without_extension = ".".join(section_name.split(".")[:-1])
            note_file_path = os.path.join(
                note_dir, f"{section_name_without_extension}.md"
            )

            # Check if the file already exists
            if os.path.exists(note_file_path):
                print(f"Section notes [{note_file_path}]: already exists, skipping")
                continue

            print(f"Section notes [{note_file_path}]: does not exist, generating")

            # Load transcript
            with open(transcript_file_path, "r", encoding="utf-8") as f:
                transcript = f.read()

            # Generate notes
            start_time = time.time()
            part_notes = generator.query_note(transcript, style, model)
            end_time = time.time()
            print(f"Note generation took {end_time - start_time:.2f} seconds")

            # Save to a single file
            with open(note_file_path, "w", encoding="utf-8") as f:
                f.write(part_notes)

        # Generate complete notes by concatenating all part notes
        complete_notes = []
        for generated_section_name in os.listdir(note_dir):
            if generated_section_name == "complete_notes.md":
                continue
            note_file_path = os.path.join(note_dir, generated_section_name)
            with open(note_file_path, "r", encoding="utf-8") as f:
                complete_notes.append(f.read())

        complete_notes = "\n\n".join(complete_notes)

        # Save to a single file
        note_file_path = os.path.join(note_dir, "complete_notes.md")
        with open(note_file_path, "w", encoding="utf-8") as f:
            f.write(f"# {course_name} Course Notes\n\n")
            f.write(complete_notes)

    except Exception as e:
        print(f"Error generating course notes: {str(e)}")

import ollama
import time
import requests
import os

model_name="gpt-oss:20b"
# model_name="qwen3:14b"
system_prompt_file="../prompt/영상요약프론프트.md"
prompt_file="../영상자막파일/이 대통령 ＂모든 산재 사망사고 직보하라＂…업무 복귀 후 첫 지시 外 8⧸9(토) ⧸ SBS 8뉴스 [bgkdFpGzwBc].srt"
result_file="./result.md"

def chat(chatmsg, system_prompt="", temperature=0.5):
    try:
        messages = []
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        messages.append({
            'role': 'user',
            'content': chatmsg
        })
        
        start_time = time.time()
        res = ollama.chat(
            model=model_name,
            messages=messages,
            options={
                'temperature': temperature
            }
        )
        end_time = time.time()
        response_time = end_time - start_time
        
        # print(res)
        return res['message']['content'], response_time
    except Exception as e:
        return f"오류 발생: {e}", 0

def main():
    """
    Main function to read prompts, get chat completion, and save the result.
    """
    try:
        # Read system prompt
        with open(system_prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()

        # Read user prompt
        with open(prompt_file, 'r', encoding='utf-8') as f:
            user_prompt = f.read()

        # Get chat completion
        print("Ollama API를 호출합니다...")
        response, response_time = chat(user_prompt, system_prompt)
        print(f"응답 시간: {response_time:.2f}초")

        # Save result to file
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(response)
        
        print(f"결과가 '{result_file}' 파일에 저장되었습니다.")

    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()

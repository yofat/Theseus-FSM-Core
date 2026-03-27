import ollama
import config

class VictimAgent:
    def __init__(self):
        self.history = [{"role": "system", "content": config.VICTIM_SYSTEM_PROMPT}]
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def chat(self, user_input):
        
        self.history.append({"role": "user", "content": user_input})
        
        response = ollama.chat(model=config.VICTIM_MODEL, messages=self.history)
        reply = response['message']['content']
        
        # Extract token counts from response if available
        prompt_tokens = response.get('prompt_eval_count', 0)
        completion_tokens = response.get('eval_count', 0)
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        
        self.history.append({"role": "assistant", "content": reply})
        return reply, prompt_tokens, completion_tokens

    def get_token_stats(self):
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens
        }

    def reset(self):
        self.history = [{"role": "system", "content": config.VICTIM_SYSTEM_PROMPT}]
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
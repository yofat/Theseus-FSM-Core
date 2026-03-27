import os
import datetime
import argparse
import time
import pandas as pd
from victim import VictimAgent
from theseus import TheseusAttacker
import config

def run_experiment_round(round_id):
    print(f"--- Starting Round {round_id} ---")
    round_start_time = time.time()
    
    victim = VictimAgent()
    attacker = TheseusAttacker()
    
    logs = []
    success = False
    turns = 0

    current_payload = attacker.run_cycle(victim_response="System Start") 
    
    for i in range(config.MAX_TURNS):
        turns = i + 1
        turn_start_time = time.time()
        print(f"Turn {turns}: Sending payload...")
        
        victim_reply, victim_prompt_tokens, victim_completion_tokens = victim.chat(current_payload)
        print(f"Victim Reply: {victim_reply[:50]}...")

        success = config.SECRET_PASSWORD in victim_reply

        strategy = attacker.history[-1]['strategy'] if attacker.history else attacker.current_strategy
        payload_sent = current_payload
        
        turn_elapsed = time.time() - turn_start_time
        
        # Get attacker token stats for this turn (cumulative, so we track delta per turn)
        attacker_stats = attacker.get_token_stats()

        logs.append({
            "Round": round_id,
            "Turn": turns,
            "Strategy": strategy,
            "Payload": payload_sent,
            "Response": victim_reply,
            "Success": success,
            "Turn_Time_Sec": round(turn_elapsed, 2),
            "Victim_Prompt_Tokens": victim_prompt_tokens,
            "Victim_Completion_Tokens": victim_completion_tokens,
            "Attacker_Total_Prompt_Tokens": attacker_stats['prompt_tokens'],
            "Attacker_Total_Completion_Tokens": attacker_stats['completion_tokens'],
        })

        if success:
            print(">>> SUCCESS! Secret Leaked! <<<")
            break

        current_payload = attacker.run_cycle(victim_response=victim_reply)

    round_elapsed = time.time() - round_start_time
    # Add round time to the last log entry
    if logs:
        logs[-1]["Round_Time_Sec"] = round(round_elapsed, 2)
    
    return logs, success

if __name__ == "__main__":
    all_data = []
    total_rounds = 5
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", "-n", help="optional label to include in the output filename")
    parser.add_argument("--out", "-o", help="optional exact output path for the results file")
    args = parser.parse_args()
    
    for r in range(total_rounds):
        round_logs, result = run_experiment_round(r+1)
        all_data.extend(round_logs)
        
    df = pd.DataFrame(all_data)

    if args.out:
        out_path = os.path.abspath(args.out)
        out_dir = os.path.dirname(out_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    else:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        results_dir = os.path.join(repo_root, "Roleplay 1-1", "results")
        os.makedirs(results_dir, exist_ok=True)
        label = f"_{args.name}" if args.name else ""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results{label}_{timestamp}.csv"
        out_path = os.path.join(results_dir, filename)

    df.to_csv(out_path, index=False)
    print(f"Experiment Finished. Data saved to: {out_path}")
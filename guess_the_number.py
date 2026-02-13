import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_rank(score):
    if score >= 500:
        return "👑 Legend"
    elif score >= 350:
        return "🔥 Pro"
    elif score >= 200:
        return "⚡ Skilled"
    else:
        return "🎯 Beginner"

def draw_progress_bar(guessed_numbers, target_range=100):
    bar_length = 20
    guessed_count = min(len(guessed_numbers), bar_length)
    progress = '#' * guessed_count + '-' * (bar_length - guessed_count)
    print(f"📊 Progress: |{progress}| {len(guessed_numbers)}/{target_range}")

def play_round(high_score, total_stats):
    clear_screen()
    print("🎮 Smart Number Guessing Game - Enhanced Edition! 🎮")
    print("🤖 I've locked a number between 1 and 100.")
    
    # Themed modes for variety
    print("\n🎨 Choose mode: 1) Classic 2) Speed Run 3) Extreme")
    mode = input("Enter choice (1-3): ").strip()
    if mode == "2":
        range_max = 50
        attempts = 7
        score_mult = 20
        time_lim = 20
        print("⚡ Speed Run: Smaller range, less time!")
    elif mode == "3":
        range_max = 200
        attempts = 4
        score_mult = 25
        time_lim = 40
        print("💥 Extreme: Bigger range, hardcore!")
    else:
        range_max = 100
        attempts = 8
        score_mult = 12
        time_lim = 30
        print("✅ Classic mode.")
    
    random_number = random.randint(1, range_max)
    guessed_numbers = set()
    streak = 0
    powerups = {"double": 1, "hint": 1}  # Earnable power-ups
    multiplier = 1.0
    start_time = time.time()
    
    while attempts > 0:
        remaining_time = int(time_lim - (time.time() - start_time))
        if remaining_time <= 0:
            print("\n⏰ Time's up!")
            break
        
        draw_progress_bar(guessed_numbers, range_max)
        print(f"\n❤️ Lives: {attempts} | ⏱️ Time: {remaining_time}s | 🔥 Streak: {streak} | x{multiplier:.1f}")
        print(f"⭐ Power-ups: Double ({powerups['double']}) | Hint ({powerups['hint']})")
        
        # Power-up choice
        pu_choice = input("Use power-up? (d/h/n): ").lower()
        if pu_choice == 'd' and powerups['double'] > 0:
            multiplier *= 2
            powerups['double'] -= 1
            print("💰 Score doubled this turn!")
        elif pu_choice == 'h' and powerups['hint'] > 0:
            digit = str(random_number)[0]
            print(f"🔮 Power hint: Starts with {digit}!")
            powerups['hint'] -= 1
            time.sleep(1)
        
        try:
            guess = int(input("🔢 Your guess: "))
        except ValueError:
            print("❌ Numbers only!")
            continue
        
        if not (1 <= guess <= range_max):
            print(f"🚫 Between 1-{range_max}!")
            continue
        if guess in guessed_numbers:
            print("⚠️ No repeats!")
            attempts -= 1
            continue
        
        guessed_numbers.add(guess)
        diff = abs(guess - random_number)
        attempts -= 1
        
        if guess == random_number:
            time_taken = time_lim - remaining_time
            score = int((attempts + 1) * score_mult * multiplier + (remaining_time * 3) + (streak * 15) - (time_taken * 2))
            print(f"\n🎉 WIN! Number: {random_number}")
            print(f"🏆 Round Score: {score} | Rank: {get_rank(score)}")
            
            total_stats['rounds'] += 1
            total_stats['total_score'] += score
            total_stats['wins'] += 1
            
            if score > high_score:
                print("🌟 NEW HIGH SCORE!")
                high_score = score
            break
        
        # Dynamic feedback with streak building
        if diff <= 2:
            streak += 1
            print("🎯 ICE COLD! (Extremely close)")
            powerups['double'] = min(2, powerups['double'] + 1)  # Reward streak
        elif diff <= 6:
            streak += 1
            print("🧊 COLD! (Close)")
        elif diff <= 15:
            streak = max(0, streak - 1)
            print("🌡️ WARM (Getting there)")
        else:
            streak = 0
            print("🥶 FREEZING! (Way off)")
        
        print("⬆️ HIGH" if guess > random_number else "⬇️ LOW")
        
        # Progressive hints
        if attempts == 4:
            parity = "EVEN" if random_number % 2 == 0 else "ODD"
            print(f"💡 Hint: {parity}")
        elif attempts == 2:
            hint_range = (max(1, random_number - 15), min(range_max, random_number + 15))
            print(f"💡 Hint: {hint_range[0]}-{hint_range[1]}")
        elif attempts == 1:
            print(f"🎲 Final lucky hint: Divisible by {random_number % 10 + 1}? No wait... guess smart!")
    
    else:
        print(f"\n💀 Game Over! Number was {random_number}")
        total_stats['rounds'] += 1
    
    print(f"\n📈 High Score: {high_score} | Avg Score: {total_stats['total_score'] // max(1, total_stats['rounds'])}")
    return high_score, total_stats

# Main game
def main():
    high_score = 0
    total_stats = {'rounds': 0, 'wins': 0, 'total_score': 0}
    
    while True:
        high_score, total_stats = play_round(high_score, total_stats)
        print("\n" + "="*50)
        again = input("🔄 Play again? (y/n): ").lower()
        if again != 'y':
            win_rate = (total_stats['wins'] / max(1, total_stats['rounds']) * 100)
            print(f"\n👋 Final Stats: {total_stats['wins']}/{total_stats['rounds']} wins ({win_rate:.0f}%) | Total Score: {total_stats['total_score']}")
            break
        clear_screen()

if __name__ == "__main__":
    main()

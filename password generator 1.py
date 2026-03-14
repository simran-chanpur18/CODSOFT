import secrets
import string
import os

# Optional: for clipboard copy
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def get_character_pool(complexity, exclude_ambiguous):
    """Return (characters, description, category_dict) based on complexity."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    ambiguous = "0OIl1|5S2Z"  # characters often confused

    if exclude_ambiguous:
        lowercase = ''.join(c for c in lowercase if c not in ambiguous)
        uppercase = ''.join(c for c in uppercase if c not in ambiguous)
        digits = ''.join(c for c in digits if c not in ambiguous)
        symbols = ''.join(c for c in symbols if c not in ambiguous)

    # Define pools based on complexity
    if complexity == 'low':
        pool = lowercase
        desc = "lowercase letters only"
        categories = {'lower': lowercase}
    elif complexity == 'medium':
        pool = lowercase + uppercase + digits
        desc = "letters (case-sensitive) and digits"
        categories = {'lower': lowercase, 'upper': uppercase, 'digit': digits}
    elif complexity == 'high':
        pool = lowercase + uppercase + digits + symbols
        desc = "letters, digits, and symbols"
        categories = {'lower': lowercase, 'upper': uppercase, 'digit': digits, 'symbol': symbols}
    else:
        # default medium
        pool = lowercase + uppercase + digits
        desc = "letters (case-sensitive) and digits"
        categories = {'lower': lowercase, 'upper': uppercase, 'digit': digits}

    if exclude_ambiguous:
        desc += " (no ambiguous characters)"
    return pool, desc, categories

def generate_password(length, pool):
    """Generate a cryptographically secure random password."""
    return ''.join(secrets.choice(pool) for _ in range(length))

def generate_strict_password(length, categories):
    """
    Generate a password that contains at least one character from each category.
    categories: dict like {'lower': 'abc...', 'upper': 'ABC...', ...}
    """
    if length < len(categories):
        raise ValueError(f"Length too short to include all categories (need at least {len(categories)})")
    
    while True:
        # Fill the password with random chars from the combined pool
        combined_pool = ''.join(categories.values())
        pwd = list(generate_password(length, combined_pool))
        
        # Check if all categories are present
        missing = [cat for cat, chars in categories.items() 
                   if not any(c in chars for c in pwd)]
        if not missing:
            return ''.join(pwd)
        # Otherwise try again

def generate_multiple_passwords(count, length, pool, strict=False, categories=None):
    """Generate multiple passwords, optionally enforcing strict category inclusion."""
    passwords = []
    for _ in range(count):
        if strict and categories:
            try:
                pwd = generate_strict_password(length, categories)
            except ValueError as e:
                print(f"Error: {e}. Using non-strict mode for this batch.")
                pwd = generate_password(length, pool)
        else:
            pwd = generate_password(length, pool)
        passwords.append(pwd)
    return passwords

def save_passwords_to_file(passwords, filename="passwords.txt"):
    """Append passwords to a file, each on a new line."""
    try:
        with open(filename, 'a') as f:
            for pwd in passwords:
                f.write(pwd + '\n')
        print(f"✅ Passwords saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save: {e}")

def copy_to_clipboard(text):
    """Copy text to clipboard if pyperclip is available."""
    if CLIPBOARD_AVAILABLE:
        pyperclip.copy(text)
        print("📋 Password copied to clipboard!")
    else:
        print("⚠️  pyperclip not installed. Install with: pip install pyperclip")

def display_passwords(passwords):
    """Display numbered list of passwords."""
    print("\n" + "-" * 40)
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}: {pwd}")
    print("-" * 40)

def main():
    print("=" * 50)
    print("    UNIQUE PASSWORD GENERATOR (MULTI-FUNCTION)")
    print("=" * 50)
    print("Generate strong, customizable passwords.\n")

    while True:  # Outer session loop
        # --- Step 1: Get basic settings ---
        while True:
            try:
                length = int(input("Enter desired password length (e.g., 12): "))
                if length < 1:
                    print("Length must be at least 1.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("\nComplexity levels:")
        print("  low    - only lowercase letters")
        print("  medium - letters (upper+lower) and digits")
        print("  high   - letters, digits, and symbols")
        while True:
            complexity = input("Choose complexity (low/medium/high) [default: medium]: ").strip().lower()
            if complexity == "":
                complexity = "medium"
            if complexity in ('low', 'medium', 'high'):
                break
            print("Invalid choice. Enter low, medium, or high.")

        exclude = input("Exclude ambiguous characters (0,O,I,l, etc.)? (y/n) [default: n]: ").strip().lower()
        exclude_ambiguous = exclude.startswith('y')

        pool, desc, categories = get_character_pool(complexity, exclude_ambiguous)
        print(f"\nCharacter set: {desc} (size {len(pool)} characters)")

        # Strict mode option
        strict = False
        if complexity in ('medium', 'high'):
            strict_input = input("Strict mode (ensure at least one of each type)? (y/n) [default: n]: ").strip().lower()
            strict = strict_input.startswith('y')

        # --- Step 2: Batch generation count ---
        while True:
            try:
                count = int(input("How many passwords to generate at once? (1-10) [default: 1]: ") or "1")
                if 1 <= count <= 10:
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Using default 1.")
                count = 1
                break

        # --- Step 3: Generate and select password ---
        while True:  # Inner loop for regeneration of the batch
            try:
                passwords = generate_multiple_passwords(count, length, pool, strict, categories)
            except ValueError as e:
                print(f"Error: {e}. Switching to non-strict for this batch.")
                passwords = generate_multiple_passwords(count, length, pool, strict=False)

            display_passwords(passwords)

            action = input("\nEnter number to select a password, 'r' to regenerate, or 'q' to quit this session: ").strip().lower()
            if action == 'r':
                continue
            elif action == 'q':
                break  # exit inner loop, go to outer (maybe ask for another session)
            else:
                try:
                    idx = int(action) - 1
                    if 0 <= idx < len(passwords):
                        selected = passwords[idx]
                        print(f"\n✅ You selected: {selected}")
                        break
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input. Use number, 'r', or 'q'.")

        if action == 'q':
            # They quit the inner loop without selecting? Actually 'q' would have broken to here
            # If they quit, we still ask if they want a new session
            pass
        else:
            # --- Step 4: Post-selection actions (copy/save) ---
            while True:
                print("\nWhat would you like to do with this password?")
                print("  c - Copy to clipboard")
                print("  s - Save to file (passwords.txt)")
                print("  b - Both copy and save")
                print("  n - Nothing, just continue")
                post = input("Your choice [default: n]: ").strip().lower()
                if post in ('', 'n'):
                    break
                elif post == 'c':
                    copy_to_clipboard(selected)
                    break
                elif post == 's':
                    save_passwords_to_file([selected])
                    break
                elif post == 'b':
                    copy_to_clipboard(selected)
                    save_passwords_to_file([selected])
                    break
                else:
                    print("Invalid choice.")

        # --- Step 5: Another session? ---
        again = input("\nGenerate another password (with new settings)? (y/n) [default: n]: ").strip().lower()
        if not again.startswith('y'):
            print("\nGoodbye! Stay secure.")
            break
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()

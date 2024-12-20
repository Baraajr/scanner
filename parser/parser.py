class RecursiveDescentParser:
    def __init__(self):
        self.grammar = {}

    def input_grammar(self):
        """Take grammar input with clear prompts."""
        self.grammar = {'S': [], 'B': []}  # Fixed non-terminals: S and B
        print("\n🟡 Enter Grammar Rules 🟡")
        for non_terminal in self.grammar.keys():
            for i in range(1, 3):
                rule = input(f"Enter rule number {i} for non-terminal '{non_terminal}': ").strip()
                self.grammar[non_terminal].append(rule)
        print("\n🟡 Defined Grammar 🟡")
        for nt, rules in self.grammar.items():
            print(f"{nt} -> {' | '.join(rules)}")

    def is_simple_grammar(self):
      """Check if the grammar is simple as per the rules."""
      for non_terminal, rules in self.grammar.items():
          seen_terminals = set()  # To track terminals that start each rule

          for rule in rules:
              if not rule:  # Rule can't be empty
                  return False

              first_char = rule[0]

              # Rule must start with a terminal
              if not first_char.islower():
                  return False

              # Check disjoint rule condition
              if first_char in seen_terminals:
                  return False  # Two rules start with the same terminal
              seen_terminals.add(first_char)

      return True

    def parse(self, sequence):
        """Recursive descent parsing function to validate the input sequence."""
        def parse_helper(stack, input_seq):
            if not stack and not input_seq:  # Both stack and input empty: Success
                return True
            if not stack or not input_seq:  # One of them is empty: Failure
                return False

            current = stack.pop(0)

            if current.isupper():  # Non-terminal
                for rule in self.grammar.get(current, []):
                    if rule[0] == input_seq[0] or rule[0].isupper():
                        # Push rule into stack and continue
                        new_stack = list(rule) + stack
                        if parse_helper(new_stack, input_seq.copy()):
                            return True
                return False
            elif current == input_seq[0]:  # Terminal matches
                input_seq.pop(0)
                return parse_helper(stack, input_seq)
            else:
                return False

        return parse_helper(['S'], list(sequence))

    def start(self):
        """Main menu-driven function for grammar input and parsing."""
        while True:
            self.input_grammar()

            if not self.is_simple_grammar():
                print("\nThe Grammar isn't simple. Please enter a valid simple grammar.\n")
                continue  # Prompt again until a valid grammar is entered

            print("\nThe Grammar is simple and valid!")

            while True:
                print("\n1- Another Grammar\n2- Another String\n3- Exit")
                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    break  # Restart grammar input
                elif choice == "2":
                    sequence = input("Enter the string want to be checked: ").strip()
                    print(f"The input String: {list(sequence)}")
                    if self.parse(sequence):
                        print("Your input String is Accepted.")
                    else:
                        print("Your input String is Rejected.")
                elif choice == "3":
                    print("Exiting...")
                    return
                else:
                    print("Invalid choice. Try again!")


# Run the program
if __name__ == "__main__":
    parser = RecursiveDescentParser()
    parser.start()

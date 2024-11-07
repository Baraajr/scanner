import re

class TokenMapper:
    # Define token mappings for keywords, operators, special characters, and comments
    token_mapper = {
        # Common Keywords
        "auto": "Keyword", "break": "Keyword", "case": "Keyword", "char": "Keyword", 
        "continue": "Keyword", "const": "Keyword", "default": "Keyword", "do": "Keyword", 
        "double": "Keyword", "else": "Keyword", "enum": "Keyword", "extern": "Keyword", 
        "float": "Keyword", "for": "Keyword", "goto": "Keyword", "if": "Keyword", 
        "int": "Keyword", "long": "Keyword", "register": "Keyword", "return": "Keyword", 
        "short": "Keyword", "signed": "Keyword", "sizeof": "Keyword", "static": "Keyword", 
        "struct": "Keyword", "switch": "Keyword", "typedef": "Keyword", "union": "Keyword", 
        "unsigned": "Keyword", "void": "Keyword", "volatile": "Keyword", "while": "Keyword", 
        "cout": "Keyword",
        
        # Common Operators
        "+": "Operator", "-": "Operator", "*": "Operator", "/": "Operator", "%": "Operator", 
        "=": "Operator", "!": "Operator", "&&": "Operator", "||": "Operator", "<": "Operator", 
        ">": "Operator", "<=": "Operator", "<<": "Operator", ">>": "Operator", ">=": "Operator", 
        "==": "Operator", "!=": "Operator",
        
        # Common Special Characters
        "(": "Special Character", ")": "Special Character", "{": "Special Character", 
        "}": "Special Character", ";": "Special Character", "'": "Special Character", 
        "\"": "Special Character", ":": "Special Character"
    }

    @staticmethod
    def check_token(token):
        # If the token is identified as a comment, treat it as such
        if token.startswith("Comment:"):
            return "Comment"
        # Check if token is in the predefined mappings
        if token in TokenMapper.token_mapper:
            return TokenMapper.token_mapper[token]
        # Check if token matches identifier or numeric constant pattern
        return TokenMapper.check_token_identifier(token)

    @staticmethod
    def check_token_identifier(token):
        # Pattern for identifiers (starting with letter or underscore, followed by alphanumeric or underscore characters)
        if re.match(r"\b[A-Za-z_][A-Za-z0-9_]*\b", token):
            return "Identifier"
        # Pattern for numeric constants (integer or float)
        if re.match(r"^\d+(\.\d+)?$", token):
            return "Numeric Constant"
        return None


class Text2TokenList:
    @staticmethod
    def convert_text_to_token_list(text):
        tokens = []
        lines = text.splitlines()  # Split the input text into lines
        
        inside_multiline_comment = False
        multiline_comment_text = ""
        
        for line in lines:
            line = line.strip()

            # Handling multi-line comments: If we are inside a comment, continue skipping lines
            if inside_multiline_comment:
                multiline_comment_text += " " + line.strip()  # Concatenate the multi-line comment content
                if "*/" in line:  # End of multi-line comment
                    tokens.append(f"Comment: {multiline_comment_text.strip()}")
                    inside_multiline_comment = False
                    multiline_comment_text = ""
                continue
            
            # Check for multi-line comment start
            if "/*" in line:
                inside_multiline_comment = True
                multiline_comment_text += " " + line.split("/*")[1].strip()  # Start capturing the multi-line comment
                if "*/" in line:  # If the comment ends in the same line
                    tokens.append(f"Comment: {multiline_comment_text.strip()}")
                    inside_multiline_comment = False
                    multiline_comment_text = ""
                continue

            # Check for single-line comment (starts with //)
            if "//" in line:
                # Split the line into code and comment parts
                code_part = line.split("//")[0].strip()  # Code before the comment
                comment_part = line.split("//")[1].strip()  # The actual comment part
                
                # Tokenize the code part
                line_tokens = re.findall(r"\b\w+\b|[^\w\s]", code_part)
                tokens.extend(line_tokens)
                
                # Add the comment part
                tokens.append(f"Comment: {comment_part}")
                continue

            # Tokenize line with regex (split keywords, operators, identifiers, numbers, and special chars)
            line_tokens = re.findall(r"\b\w+\b|[^\w\s]", line)
            tokens.extend(line_tokens)

        return tokens


def test_token_mapping():
    print("Please enter your text (type 'END' on a new line to finish):")

    # Collect multi-line input from the user
    input_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":  # Use 'END' to finish the input
            break
        input_lines.append(line)
    
    # Join the input lines into a single string
    text = "\n".join(input_lines)

    # Step 2: Convert the text to tokens
    tokens = Text2TokenList.convert_text_to_token_list(text)
    
    # Step 3: Check each token
    for token in tokens:
        token_type = TokenMapper.check_token(token)
        print(f"Token: {token}, Type: {token_type}")

    # Add this to keep the console window open after the program finishes
    input("Press Enter to exit...")  # This will wait for the user to press Enter before closing


if __name__ == "__main__":
    test_token_mapping()

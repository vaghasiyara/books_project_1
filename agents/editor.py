# agents/editor.py
class HumanEditor:
    def get_feedback(self, spun_text, ai_review):
        print("\n=== AI-Generated Chapter ===")
        print(spun_text)
        print("\n=== AI Review ===")
        print(ai_review)
        
        print("\nProvide your feedback (type 'done' when finished):")
        feedback = []
        while True:
            line = input("> ")
            if line.lower() == 'done':
                break
            feedback.append(line)
            
        return "\n".join(feedback)
    
    def final_approval(self, final_text):
        print("\n=== Final Chapter Version ===")
        print(final_text)
        approval = input("Approve this version? (y/n): ")
        return approval.lower() == 'y'
import fitz
import re
import json
import html

doc = fitz.open(r'c:\Users\Thefr\Dropbox\Komputer\Downloads\Baza pytań _ Dyskretna-Machen.pdf')
full_text = ''
for page in doc:
    full_text += page.get_text()

# Parsowanie pytań
questions = []
# Znajdź wszystkie pytania
pattern = r'Pytanie (\d+): (.+?)(?=Pytanie \d+:|5\.02\.2026|$)'
matches = re.findall(pattern, full_text, re.DOTALL)

for match in matches:
    q_num = int(match[0])
    content = match[1].strip()
    
    # Podziel na pytanie i odpowiedzi
    # Szukamy pierwszego ○ lub ✓
    first_option = re.search(r'[○✓]', content)
    if first_option:
        question_text = content[:first_option.start()].strip()
        options_text = content[first_option.start():]
        
        # Parsuj opcje
        options = []
        # Split by option markers
        option_parts = re.split(r'(?=[○✓])', options_text)
        for part in option_parts:
            part = part.strip()
            if not part:
                continue
            is_correct = part.startswith('✓')
            option_text = part[1:].strip()
            # Czyść tekst z danych strony
            option_text = re.sub(r'5\.02\.2026.*?Baza pytań.*?baza\.php.*?\d+/\d+', '', option_text, flags=re.DOTALL)
            option_text = option_text.strip()
            if option_text:
                options.append({
                    'text': option_text,
                    'correct': is_correct
                })
        
        if options:
            # Usuń footery ze stron
            question_text = re.sub(r'5\.02\.2026.*?Baza pytań.*?baza\.php.*?\d+/\d+', '', question_text, flags=re.DOTALL)
            question_text = question_text.strip()
            
            questions.append({
                'id': q_num,
                'question': question_text,
                'options': options,
                'multiple': sum(1 for o in options if o['correct']) > 1
            })

print(f"Znaleziono {len(questions)} pytań")

# Zapisz do JSON
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Pytania zapisane do questions.json")

# Pokaż kilka pierwszych pytań
for q in questions[:3]:
    print(f"\n=== Pytanie {q['id']} ===")
    print(f"Treść: {q['question'][:100]}...")
    print(f"Liczba opcji: {len(q['options'])}")
    print(f"Wielokrotny wybór: {q['multiple']}")

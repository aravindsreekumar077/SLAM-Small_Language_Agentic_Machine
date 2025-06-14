import random
import csv
import inflect

# Define categories and corresponding templates
categories = {
    "arithmetic": [
        ("What is {} plus {}?", "{} + {}"),
        ("Calculate the sum of {} and {}", "{} + {}"),
        ("How much is {} minus {}?", "{} - {}"),
        ("What is the product of {} and {}?", "{} * {}"),
        ("Divide {} by {}", "{} / {}"),
        ("What is {} multiplied by {}?", "{} * {}"),
        ("Subtract {} from {}", "{} - {}"),
        ("Add {} to {}", "{} + {}"),
        ("What is the quotient of {} and {}?", "{} / {}"),
        ("What is {} times {}?", "{} * {}"),
    ],
    "exponents": [
        ("What is {} squared?", "{} ** 2"),
        ("What is {} cubed?", "{} ** 3"),
        ("Calculate {} to the power of {}", "{} ** {}"),
        ("What is the square of {}?", "{} ** 2"),
        ("What is the cube of {}?", "{} ** 3"),
    ],
    "roots": [
        ("What is the square root of {}?", "sqrt({})"),
        ("Find the cube root of {}", "cbrt({})"),
        ("Calculate the {}th root of {}", "{}th_root({})"),
    ],
    "percentages": [
        ("What is {} percent of {}?", "({} / 100) * {}"),
        ("Increase {} by {} percent", "{} * (1 + ({} / 100))"),
        ("Decrease {} by {} percent", "{} * (1 - ({} / 100))"),
        ("{} is what percent of {}?", "({} / {}) * 100"),
    ],
    "averages": [
        ("What is the average of {}, {}, and {}?", "({} + {} + {}) / 3"),
        ("Calculate the mean of {}, {}, {}, and {}", "({} + {} + {} + {}) / 4"),
    ],
    "comparisons": [
        ("Which is greater, {} or {}?", "max({}, {})"),
        ("Which is smaller, {} or {}?", "min({}, {})"),
        ("Is {} greater than {}?", "{} > {}"),
        ("Is {} less than {}?", "{} < {}"),
    ],
    "mixed_operations": [
        ("What is {} plus {} times {}?", "{} + ({} * {})"),
        ("Calculate {} minus {} divided by {}", "{} - ({} / {})"),
        ("Add {} to the product of {} and {}", "{} + ({} * {})"),
        ("Subtract {} from the sum of {} and {}", "({} + {}) - {}"),
    ],
    "fractions": [
        ("What is half of {}?", "{} / 2"),
        ("What is one third of {}?", "{} / 3"),
        ("What is {} divided by {}?", "{} / {}"),
        ("What is {} over {}?", "{} / {}"),
    ],
    "tables": [
        (
            "Write table of {}", 
            "Write table of {} with each line containing '{} x n = result' for n from 1 to 10"
        ),
        (
            "Give me the multiplication table of {}", 
            "Write table of {} with each line containing '{} x n = result' for n from 1 to 10"
        ),
        (
            "Show the table for {}", 
            "Write table of {} with each line containing '{} x n = result' for n from 1 to 10"
        ),
    ]
}

# Function to generate synthetic data
def generate_data(num_samples):
    data = []
    for _ in range(num_samples):
        category = random.choice(list(categories.keys()))
        #print(category)
        template, simplified = random.choice(categories[category])
        num_placeholders = max(template.count("{}"), simplified.count("{}"))
        if(category == "tables"):
            num_placeholders = 1  # For table questions, we only need one number

        nums = [random.randint(1, 10000) for _ in range(num_placeholders)]
        # Randomly decide whether to use digits or words for each number
        def num_to_word(n):
            p = inflect.engine()
            return p.number_to_words(n)

        # Use only as many numbers as needed for the template
        nums_in_words = [num_to_word(n) if random.choice([True, False]) else n for n in nums[:template.count("{}")]]
        original = template.format(*nums_in_words)
        # For tables, ensure the same number is used in both places in the simplified template
        if category == "tables":
            simplified_form = f"calculate the expression: {simplified.format(nums[0], nums[0])}"
        else:
            simplified_form = f"calculate the expression: {simplified.format(*nums[:simplified.count('{}')])}"
        #print(simplified.count('{}'), nums[:simplified.count('{}')])
        #print(original, simplified_form, category)
        data.append((original, simplified_form, category))
    return data


# Main function to run the script
def main():
   num_samples = 50000  # Set to 50000 for full dataset
   output_file = "math_prompt_refinement_dataset.csv"
   dataset = generate_data(num_samples)
   # Save to CSV
   with open(output_file, mode='w', newline='', encoding='utf-8') as file:
       writer = csv.writer(file)
       writer.writerow(["Original Question", "Simplified Form", "Category"])
       writer.writerows(dataset)
   print(f"Dataset of {num_samples} samples saved to: {output_file}")
   
if __name__ == "__main__":
   main()
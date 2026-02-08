# test_providers.py
"""
Main Testing Module for Gemini & Ollama Providers
Test both providers with common questions and compare responses
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
from rag_engine import RAGEngine
from gemini_provider import GeminiProvider
from ollama_provider import OllamaProvider
from database import Database

# ============================================
# COMMON TEST QUESTIONS
# ============================================

TEST_QUESTIONS = [
    "What is Alice Johnson's GPA and major?",
    "Which students are enrolled in CS101?",
    "Tell me about Carol Davis's academic performance",
    "What courses does Bob Smith take?",
    "Who teaches Machine Learning Fundamentals?",
    "List the grades for Alice Johnson in all courses",
    "What is the prerequisite structure for Computer Science courses?",
    "Compare the GPAs of all students and identify the top performer"
]

# ============================================
# TEST RESULTS TRACKER
# ============================================

class TestResults:
    """Track and analyze test results"""

    def __init__(self):
        self.results = {
            "gemini": [],
            "ollama": []
        }
        self.metadata = {
            "timestamp": datetime.now().isoformat(),
            "test_count": len(TEST_QUESTIONS)
        }

    def add_result(self, provider: str, question: str, response: str,
                   latency: float, success: bool):
        """Add a test result"""
        self.results[provider].append({
            "question": question,
            "response": response,
            "latency": latency,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })

    def get_summary(self, provider: str) -> Dict:
        """Get summary statistics for a provider"""
        results = self.results[provider]
        if not results:
            return {"error": "No results"}

        successful = sum(1 for r in results if r["success"])
        total_latency = sum(r["latency"] for r in results)
        avg_latency = total_latency / len(results) if results else 0

        return {
            "provider": provider,
            "total_tests": len(results),
            "successful": successful,
            "success_rate": f"{(successful/len(results)*100):.1f}%",
            "total_latency": f"{total_latency:.2f}s",
            "avg_latency": f"{avg_latency:.2f}s",
            "total_response_length": sum(len(r["response"]) for r in results)
        }

    def save_to_file(self, filename: str = None):
        """Save results to JSON file"""
        if filename is None:
            filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "metadata": self.metadata,
            "results": self.results,
            "summaries": {
                "gemini": self.get_summary("gemini"),
                "ollama": self.get_summary("ollama")
            }
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        return filename

# ============================================
# PROVIDER TESTER CLASS
# ============================================

class ProviderTester:
    """Test and compare AI providers"""

    def __init__(self):
        self.db = Database()
        self.results = TestResults()
        self.available_providers = RAGEngine.get_available_providers()

    def check_providers(self) -> Dict[str, bool]:
        """Check which providers are available"""
        print("\n" + "="*70)
        print("🔍 CHECKING PROVIDER AVAILABILITY")
        print("="*70)

        availability = {
            "gemini": GeminiProvider.is_available(),
            "ollama": OllamaProvider.is_available()
        }

        for provider, available in availability.items():
            status = "✅ AVAILABLE" if available else "❌ NOT AVAILABLE"
            print(f"{provider.upper():15} : {status}")

        # Show Ollama models if available
        if availability["ollama"]:
            models = OllamaProvider.get_available_models()
            print(f"\n📦 Available Ollama Models: {', '.join(models)}")

        return availability

    def test_single_provider(self, provider: str, questions: List[str] = None,
                            ollama_model: str = None) -> Dict:
        """Test a single provider with questions"""

        if questions is None:
            questions = TEST_QUESTIONS

        print(f"\n{'='*70}")
        print(f"🧪 TESTING {provider.upper()} PROVIDER")
        print(f"{'='*70}")

        if ollama_model and provider == "ollama":
            print(f"Model: {ollama_model}")

        print(f"Questions to test: {len(questions)}\n")

        try:
            # Initialize RAG engine
            rag = RAGEngine(provider_type=provider, ollama_model=ollama_model)

            # Test each question
            for i, question in enumerate(questions, 1):
                print(f"\n[{i}/{len(questions)}] Question: {question}")
                print("-" * 70)

                start_time = time.time()

                try:
                    response = rag.query(question)
                    latency = time.time() - start_time
                    success = True

                    # Show response
                    print(f"Response ({latency:.2f}s):")
                    print(response[:300] + "..." if len(response) > 300 else response)

                    self.results.add_result(provider, question, response, latency, success)

                except Exception as e:
                    latency = time.time() - start_time
                    error_msg = str(e)
                    print(f"❌ ERROR ({latency:.2f}s): {error_msg}")
                    self.results.add_result(provider, question, error_msg, latency, False)

            return self.results.get_summary(provider)

        except Exception as e:
            print(f"\n❌ PROVIDER INITIALIZATION ERROR: {str(e)}")
            return {"error": str(e)}

    def test_all_providers(self, questions: List[str] = None) -> Dict:
        """Test all available providers"""

        if questions is None:
            questions = TEST_QUESTIONS

        print("\n" + "🚀 "*35)
        print("PROVIDER COMPARISON TEST")
        print("🚀 "*35)

        summaries = {}

        # Test Gemini
        if "gemini" in self.available_providers:
            summary = self.test_single_provider("gemini", questions)
            summaries["gemini"] = summary
        else:
            print("\n⏭️  SKIPPING GEMINI (Not configured)")

        # Test Ollama
        if "ollama" in self.available_providers:
            models = OllamaProvider.get_available_models()
            if models:
                model = models[0]  # Use first available model
                summary = self.test_single_provider("ollama", questions, model)
                summaries["ollama"] = summary
            else:
                print("\n⏭️  SKIPPING OLLAMA (No models found)")
        else:
            print("\n⏭️  SKIPPING OLLAMA (Not configured)")

        return summaries

    def print_comparison(self):
        """Print comparison of results"""
        print("\n" + "="*70)
        print("📊 COMPARISON RESULTS")
        print("="*70)

        gemini_summary = self.results.get_summary("gemini")
        ollama_summary = self.results.get_summary("ollama")

        if "error" not in gemini_summary and "error" not in ollama_summary:
            print("\n{:<20} {:<20} {:<20}".format("Metric", "Gemini", "Ollama"))
            print("-" * 70)

            print("{:<20} {:<20} {:<20}".format(
                "Total Tests",
                gemini_summary["total_tests"],
                ollama_summary["total_tests"]
            ))

            print("{:<20} {:<20} {:<20}".format(
                "Success Rate",
                gemini_summary["success_rate"],
                ollama_summary["success_rate"]
            ))

            print("{:<20} {:<20} {:<20}".format(
                "Avg Latency",
                gemini_summary["avg_latency"],
                ollama_summary["avg_latency"]
            ))

            print("{:<20} {:<20} {:<20}".format(
                "Total Latency",
                gemini_summary["total_latency"],
                ollama_summary["total_latency"]
            ))

            print("{:<20} {:<20} {:<20}".format(
                "Total Resp Length",
                gemini_summary["total_response_length"],
                ollama_summary["total_response_length"]
            ))

            print("\n" + "="*70)
            print("📈 ANALYSIS")
            print("="*70)

            gemini_latency = float(gemini_summary["avg_latency"].rstrip('s'))
            ollama_latency = float(ollama_summary["avg_latency"].rstrip('s'))

            if gemini_latency < ollama_latency:
                diff = ollama_latency - gemini_latency
                print(f"⚡ Gemini is {diff:.2f}s faster on average")
            else:
                diff = gemini_latency - ollama_latency
                print(f"⚡ Ollama is {diff:.2f}s faster on average")

            print(f"\n💾 Memory Usage (Ollama): Local - No cloud bandwidth")
            print(f"☁️  Cloud Usage (Gemini): API based - Scalable")

        else:
            print("Some providers had errors during testing")

# ============================================
# INTERACTIVE TESTING MODE
# ============================================

def interactive_test():
    """Interactive testing mode where user asks questions"""

    print("\n" + "="*70)
    print("🎯 INTERACTIVE TESTING MODE")
    print("="*70)
    print("\nAsk custom questions and test both providers")
    print("Type 'exit' to quit, 'example' for example questions\n")

    tester = ProviderTester()

    # Check providers first
    availability = tester.check_providers()

    if not any(availability.values()):
        print("\n❌ No providers available!")
        return

    while True:
        user_input = input("\nYour question: ").strip()

        if user_input.lower() == 'exit':
            break

        elif user_input.lower() == 'example':
            print("\nExample questions:")
            for i, q in enumerate(TEST_QUESTIONS, 1):
                print(f"{i}. {q}")
            continue

        if not user_input:
            continue

        # Test with available providers
        if availability["gemini"]:
            print(f"\n{'='*70}")
            print("Testing with GEMINI...")
            print(f"{'='*70}")
            try:
                rag = RAGEngine(provider_type="gemini")
                start = time.time()
                response = rag.query(user_input)
                latency = time.time() - start
                print(f"Response ({latency:.2f}s):")
                print(response)
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        if availability["ollama"]:
            print(f"\n{'='*70}")
            print("Testing with OLLAMA...")
            print(f"{'='*70}")
            try:
                models = OllamaProvider.get_available_models()
                if models:
                    rag = RAGEngine(provider_type="ollama", ollama_model=models[0])
                    start = time.time()
                    response = rag.query(user_input)
                    latency = time.time() - start
                    print(f"Response ({latency:.2f}s, Model: {models[0]}):")
                    print(response)
            except Exception as e:
                print(f"❌ Error: {str(e)}")

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main testing function"""

    print("\n" + "🎓 "*35)
    print("STUDENT RECORDS RAG - PROVIDER TESTING")
    print("🎓 "*35)

    while True:
        print("\n" + "="*70)
        print("SELECT TESTING MODE")
        print("="*70)
        print("\n1. Check Provider Availability")
        print("2. Test Gemini Only")
        print("3. Test Ollama Only")
        print("4. Compare Both Providers")
        print("5. Interactive Testing (Custom Questions)")
        print("6. Custom Test Questions")
        print("7. Exit")

        choice = input("\nSelect option (1-7): ").strip()

        if choice == "1":
            # Check availability
            tester = ProviderTester()
            tester.check_providers()

        elif choice == "2":
            # Test Gemini only
            tester = ProviderTester()
            if "gemini" in tester.available_providers:
                tester.test_single_provider("gemini")
                print("\n" + "="*70)
                print(tester.results.get_summary("gemini"))
                print("="*70)
            else:
                print("❌ Gemini not available. Configure GEMINI_API_KEY")

        elif choice == "3":
            # Test Ollama only
            tester = ProviderTester()
            if "ollama" in tester.available_providers:
                models = OllamaProvider.get_available_models()
                if models:
                    print(f"\nAvailable models: {', '.join(models)}")
                    model = input(f"Select model (default: {models[0]}): ").strip() or models[0]
                    tester.test_single_provider("ollama", ollama_model=model)
                    print("\n" + "="*70)
                    print(tester.results.get_summary("ollama"))
                    print("="*70)
                else:
                    print("❌ No Ollama models found. Run: ollama pull mistral")
            else:
                print("❌ Ollama not available. Start with: ollama serve")

        elif choice == "4":
            # Compare both providers
            tester = ProviderTester()
            tester.check_providers()
            summaries = tester.test_all_providers()
            tester.print_comparison()

            # Save results
            filename = tester.results.save_to_file()
            print(f"\n💾 Results saved to: {filename}")

        elif choice == "5":
            # Interactive mode
            interactive_test()

        elif choice == "6":
            # Custom test questions
            tester = ProviderTester()
            print("\n" + "="*70)
            print("ENTER CUSTOM QUESTIONS")
            print("="*70)
            print("Enter questions one by one (empty line to finish):\n")

            custom_questions = []
            count = 1
            while True:
                q = input(f"Question {count}: ").strip()
                if not q:
                    break
                custom_questions.append(q)
                count += 1

            if custom_questions:
                summaries = tester.test_all_providers(custom_questions)
                tester.print_comparison()
                filename = tester.results.save_to_file()
                print(f"\n💾 Results saved to: {filename}")

        elif choice == "7":
            print("\nThank you for testing! Goodbye! 👋")
            break

        else:
            print("❌ Invalid option. Please select 1-7")

# ============================================
# QUICK TEST FUNCTION (FOR DEBUGGING)
# ============================================

def quick_test():
    """Quick test - useful for debugging"""
    print("\n⚡ QUICK TEST - Single Question\n")

    question = "What is Alice's GPA?"

    # Test Gemini
    try:
        print("Testing Gemini...")
        rag = RAGEngine(provider_type="gemini")
        response = rag.query(question)
        print(f"✅ Gemini Response: {response[:200]}...")
    except Exception as e:
        print(f"❌ Gemini Error: {e}")

    # Test Ollama
    try:
        print("\nTesting Ollama...")
        models = OllamaProvider.get_available_models()
        if models:
            rag = RAGEngine(provider_type="ollama", ollama_model=models[0])
            response = rag.query(question)
            print(f"✅ Ollama Response: {response[:200]}...")
        else:
            print("❌ No Ollama models available")
    except Exception as e:
        print(f"❌ Ollama Error: {e}")

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            quick_test()
        elif sys.argv[1] == "--compare":
            tester = ProviderTester()
            tester.check_providers()
            tester.test_all_providers()
            tester.print_comparison()
            filename = tester.results.save_to_file()
            print(f"\n💾 Results saved to: {filename}")
        elif sys.argv[1] == "--interactive":
            interactive_test()
        else:
            print("Unknown option. Use --quick, --compare, or --interactive")
    else:
        # Run main interactive menu
        main()
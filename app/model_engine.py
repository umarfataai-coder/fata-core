import time

class FataModelEngine:
    def __init__(self):
        print("Ana tada injin Fata PyTorch Transformer...")

    def process_query_stream(self, prompt: str):
        # A nan gaba za mu haɗa PyTorch generate(stream=True)
        full_response = f"Fata AI Response to: '{prompt}'. Injin PyTorch yana aiki lami lafiya tare da multimodal capabilities."
        words = full_response.split(" ")
        for word in words:
            yield f"data: {word} \n\n"
            time.sleep(0.08)  # Sakamako mai sauri na dakiku

fata_engine = FataModelEngine()
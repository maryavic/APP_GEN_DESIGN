import base64
import ollama

class KeywordsExtractor:
    def __init__(self):
        """
        Initializes the Ollama Keywords Extractor.
        """
        pass

    def extract_keywords_from_image(self, image):
        """
        Extracts keywords from the uploaded image using Ollama's `llava` model.

        Args:
            image (BytesIO): Uploaded image file.

        Returns:
            list: List of extracted keywords.
        """
        encoded_image = base64.b64encode(image.getvalue()).decode('utf-8')
        
        prompt = """
        Analyze the sketch provided and extract the most important keywords or key concepts that describe its content.
        Identify key objects, themes, or any distinctive features that are visually represented. 
        Please list the most relevant keywords that summarize the sketch."
        """
        
        try:
            response = ollama.chat(
                model='llava',
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [encoded_image]
                }]
            )
            # Parse the keywords
            response_text = response['message']['content']
            keywords = [keyword.strip() for keyword in response_text.split(',') if keyword.strip()]
            return keywords
        except Exception as e:
            raise ValueError(f"Keyword extraction error: {e}")

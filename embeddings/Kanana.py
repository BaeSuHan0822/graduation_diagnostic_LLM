import torch.nn.functional as F
from transformers import AutoModel
from langchain_core.embeddings import Embeddings

class Custom_Kanana(Embeddings) :
    def __init__(
        self,
        model_name = "kakaocorp/kanana-nano-2.1b-embedding",
        instruction = "",
        device = "cpu",
        max_length = 512,
        normalize = True
    ):
        self.model = AutoModel.from_pretrained(model_name,
                                    trust_remote_code = True).to(device)
        self.instruction = instruction
        self.max_length = max_length
        self.normalize = normalize
        
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed search docs.

        Args:
            texts: List of text to embed.

        Returns:
            List of embeddings.
        """
        embeddings = self.model.encode(texts,instruction = self.instruction,max_length = self.max_length)
        if self.normalize :
            embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.tolist()
        

    def embed_query(self, text: str) -> list[float]:
        """Embed query text.

        Args:
            text: Text to embed.

        Returns:
            Embedding.
        """
        embeddings = self.model.encode(text, instruction = self.instruction, max_length = self.max_length)
        if self.normalize :
            embeddings = F.normalize(embeddings, p = 2, dim = 1)
        return embeddings[0].tolist()
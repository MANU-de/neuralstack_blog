🤖 My Emoji Generator: Gemma 3 270M-IT (ONNX)
===================

A hyper-efficient AI project that leverages Google's compact Gemma 3 270M-IT model, fine-tuned for text-to-emoji translation and optimized using ONNX for high-speed, client-side inference in a web browser.

This repository contains the code and documentation for the fine-tuning process, ONNX conversion, and a simple web demo demonstrating on-device AI.

✨ Key Features
----------

* **Ultra-Lightweight LLM:** Utilizes the 270 Million parameter version of Gemma 3 for minimal footprint.

* **Emoji Translation:** Specialized fine-tuning to convert natural language into relevant emoji sequences.

* **ONNX Optimization:** Converted for maximum efficiency using the Open Neural Network Exchange format.

* Client-Side Inference:** Designed to run entirely in the browser using the [Transformers.js](https://www.google.com/search?q=https://huggingface.co/docs/transformers.js), enabling instant, private, and cost-effective responses.

🚀 Hugging Face Model & Blog Post
-----------------

| Resource  | Description |
| ------------- |:-------------:|
| Model Repository | The optimized model is hosted on Hugging Face: [manuelaschrittwieser/myemoji-gemma-3-270m-it-onnx ](https://huggingface.co/manuelaschrittwieser/myemoji-gemma-3-270m-it-onnx) |
| Base Model | The original model from Google: [google/gemma-3-270m-it](https://huggingface.co/google/gemma-3-270m-it) |
| Blog Post | Read the full breakdown of the project on Neuralstack |

🛠️ Project Structure
----------
This repository is structured to separate the training/conversion process from the deployment demo.

[https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/Demos/Emoji-Gemma-on-Web/resources/Fine_tune_Gemma_3_270M_for_emoji_generation.ipynb](https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/Demos/Emoji-Gemma-on-Web/resources/Fine_tune_Gemma_3_270M_for_emoji_generation.ipynb)

```
my-emoji-generator/
├── training/                # Scripts and notebooks for fine-tuning
│   ├── fine-tune.ipynb      # Colab/Jupyter notebook for QLoRA fine-tuning
│   └── data/                # Sample dataset (text-to-emoji pairs)
├── deployment/              # Web application for browser demo
│   ├── index.html           # Frontend HTML structure
│   ├── script.js            # JavaScript using Transformers.js to run the model
│   └── style.css            # Basic styling
├── ONNX_conversion.ipynb    # Notebook for converting the fine-tuned model to ONNX
└── README.md                # This file
```

⚙️ Installation & Setup (Local Web Demo)
-----------------

To run the client-side demo locally, you only need a modern browser that supports WebAssembly (WASM).

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/MANU-de/neuralstack_blog.git
   cd neuralstack_blog/projects/my-emoji-generator/deployment
   ```
2. **Run a Local Server:** Since the browser demo uses JavaScript modules, you need a local web server. The simplest way is often using Python: 

```bash
python -m http.server 8000
```
3. **Access the Demo:** Open your web browser and navigate to http://localhost:8000.


💻 Usage (Code Snippet)
-----------------

The model is accessed using the `transformers.js` library.

**Prerequisites**

```bash
npm install @xenova/transformers
```

**JavaScript Example**

```javascript
import { pipeline } from '@xenova/transformers';

/**
 * Runs the model to generate emojis for a given text input.
 * @param {string} text The text to convert to emojis.
 * @returns {Promise<string>} The generated emoji sequence.
 */
async function generateEmojis(text) {
  // The generator uses the optimized ONNX model from the Hugging Face Hub
  const generator = await pipeline(
    'text-generation', 
    'manuelaschrittwieser/myemoji-gemma-3-270m-it-onnx'
  );

  const output = await generator(text, {
    max_new_tokens: 20,
    temperature: 0.7, 
    do_sample: true,
  });

  return output[0].generated_text;
}

// Test the function
generateEmojis("I can't wait for summer vacation!").then(console.log);
// Expected output: ☀️🏖️😎
```

📜 Fine-Tuning & Conversion Notes
-----------------

The fine-tuning process was achieved using **QLoRA** (Quantized Low-Rank Adaptation), allowing for efficient training on consumer-grade GPUs.

1. **Fine-Tuning:** Refer to the `training/fine-tune.ipynb` notebook for the steps on preparing the dataset and fine-tuning the base `google/gemma-3-270m-it` model.

2. **ONNX Conversion:** The fine-tuned model was converted to ONNX format. This typically involves using the `optimum` library from Hugging Face. See the `ONNX_conversion.ipynb` for details on this optimization step.

🤝 Contribution
-----------------

Feel free to open issues, submit pull requests, or share your own emoji datasets for further fine-tuning!

📄 License
-----------------

This project is built upon Google's Gemma model. By using this model, you agree to the [Gemma Terms of Use](https://ai.google.dev/gemma/terms) 

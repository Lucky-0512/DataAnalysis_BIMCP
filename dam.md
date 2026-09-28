**A limitation on my local PC pushed me into an experiment I didn't initially plan: getting multiple models to work together as one continuous conversation.**

I was building a local AI web app that needed to handle both **text and vision**.

I started with **Qwen3 1.7B through Ollama** for text.

Then I wanted to add a Qwen vision-language model.

Running both locally quickly became impractical.

So instead of asking *“How do I make my PC run both?”*, I started asking:

**“Why do they need to run on the same machine?”**

That led me to **Kaggle + Ollama + ngrok**.

I spun up an Ollama server remotely, exposed its API through ngrok, and connected it back to my local application.

Then I built the part I was actually interested in:

### A custom model router in Python.

It could:

→ Route text queries to the lightweight local model
→ Route image/attachment queries to the remote VLM
→ Switch between models based on the request
→ Carry the conversation history across those switches

So the user experiences **one continuous conversation**, while different requests can be handled by different models running in different places.

And because the models are exposed through APIs, there's no fundamental requirement that they all live on the same machine.

You could have:

**Local model → Port A**

**Remote VLM → Port B**

**Another capability → Port C**

with the application deciding which one to call.

That's the part that really clicked for me.

### Models as distributed capabilities.

Instead of thinking:

> *“I need one model capable of doing everything.”*

You can think:

> *“I have different models, each good at something, and my application decides when to use each one.”*

The remote compute doesn't necessarily have to be Kaggle either. It could be another machine, a server, or another environment capable of serving the model.

This has interesting implications for **local AI and agentic systems** — particularly when you want more control over where workloads run, while also being able to use models that your local hardware simply can't handle.

For me, the interesting part wasn't just getting a VLM running remotely.

It was **building the routing and conversation layer that made the different models feel like one system.**

Still a proof-of-concept, with plenty left before I'd call it shippable.

But this was one of those experiments where a hardware limitation forced me to rethink the architecture — and I ended up learning considerably more than I expected.

#AI #LLM #LocalAI #Ollama #Python #MultimodalAI #DistributedAI #AgenticAI #Kaggle #Ngrok

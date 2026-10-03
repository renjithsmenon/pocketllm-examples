// Streaming chat against PocketLLM Server.
//   npm install openai
//   node openai-client.mjs

import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://IPHONE_IP:8080/v1",
  apiKey: "YOUR_API_KEY",
});

const stream = await client.chat.completions.create({
  model: "local-model",
  messages: [{ role: "user", content: "Say hello in one short sentence." }],
  stream: true,
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}

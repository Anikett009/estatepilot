import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { z } from "zod";

export async function POST(req: Request) {
  try {
    const { message } = await req.json();

    // Define the expected JSON structure from Gemini
    const schema = z.object({
      guidance: z.string().describe("AI-guided startup advice based on book insights."),
      citations: z.array(
        z.object({
          book: z.string().describe("Book name"),
          page: z.string().describe("Page or blog reference."),
          anecdote: z.string().describe("Relevant lesson or story from the book."),
        })
      ).describe("List of citations with insights."),
    });

    // Construct the AI prompt
    const prompt = `
      I am a rookie startup founder. Guide me by using knowledge from these books.
      Cite the pages/open source blogs of these books which will help me build it, and give proper anecdotes:
      
      1. The Lean Startup – Eric Ries
      2. Zero to One – Peter Thiel
      3. The Hard Thing About Hard Things – Ben Horowitz
      4. Shoe Dog – Phil Knight
      5. How to Win at the Sport of Business – Mark Cuban
      6. Lost and Founder – Rand Fishkin
      7. Delivering Happiness – Tony Hsieh
      8. That Will Never Work – Marc Randolph
      9. The Everything Store – Brad Stone
      10. Made in America – Sam Walton
      
      Provide structured, concise insights in JSON format:
      {
        "guidance": "General startup advice from the books",
        "citations": [
          { "book": "Book Name", "page": "Page number", "anecdote": "Lesson learned" },
          ...
        ]
      }
    `;

    // Call Gemini API
    const result = await generateObject({
      model: google("gemini-1.5-flash"),
      system: "Provide structured startup guidance using book insights.",
      prompt,
      schema,
    });

    return result.toJsonResponse();
  } catch (error) {
    console.error("Error generating guidance:", error);
    return new Response(JSON.stringify({ error: "Failed to generate guidance" }), { status: 500 });
  }
}

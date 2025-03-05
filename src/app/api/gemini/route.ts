import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { z } from "zod";

export async function POST(req: Request) {
  try {
    const { startupName, problemStatement, targetAudience, businessModel } =
      await req.json();

    // Define structured schema for Gemini's output
    const schema = z.object({
      viabilityScore: z.number().describe("Viability score in percentage."),
      marketResearch: z.string().describe("Insights on market trends."),
      competitorAnalysis: z.string().describe("Overview of key competitors."),
      businessRecommendations: z
        .string()
        .describe("Actionable advice for business growth."),
      swot: z.object({
        strengths: z.array(z.string()).describe("List of strengths."),
        weaknesses: z.array(z.string()).describe("List of weaknesses."),
        opportunities: z.array(z.string()).describe("Market opportunities."),
        threats: z.array(z.string()).describe("Threats to the business."),
      }),
    });

    // Construct a detailed prompt for Gemini
    const prompt = `
      You are an expert startup consultant. Given the following startup idea details, provide a detailed analysis including:
      - Viability Score (0-100)
      - Market Research & Trends
      - Competitor Analysis
      - Business Recommendations
      - SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
      
      Startup Details:
      - Startup Name: ${startupName}
      - Problem Statement: ${problemStatement}
      - Target Audience: ${targetAudience}
      - Business Model: ${businessModel}

      Return only a JSON object in the following format:
      {
        "viabilityScore": number,
        "marketResearch": string,
        "competitorAnalysis": string,
        "businessRecommendations": string,
        "swot": {
          "strengths": string[],
          "weaknesses": string[],
          "opportunities": string[],
          "threats": string[]
        }
      }
    `;

    // Call Gemini API using Vercel AI SDK
    const result = await generateObject({
      model: google("gemini-1.5-flash"),
      system: "Provide startup analysis based on user input.",
      prompt,
      schema,
    });

    return result.toJsonResponse();
  } catch (error) {
    console.error("Error processing Gemini request:", error);
    return new Response(
      JSON.stringify({ error: "Failed to generate analysis" }),
      { status: 500 }
    );
  }
}

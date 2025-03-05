import { generateObject } from "ai";
import { google } from "@ai-sdk/google";
import { z } from "zod";

export async function POST(req: Request) {
  try {
    const { businessName, industry, startupCost, revenueStreams, operatingExpenses, fundingSources } = await req.json();

    // Define the expected JSON structure from Gemini
    const schema = z.object({
      roadmap: z.array(z.string()).describe("Milestones for the business."),
      revenueProjections: z.array(
        z.object({
          period: z.string().describe("Time period (e.g., Q1 2024)."),
          revenue: z.string().describe("Projected revenue."),
          growth: z.string().describe("Growth percentage."),
        })
      ),
      expenseBreakdown: z.array(
        z.object({
          category: z.string().describe("Expense category."),
          amount: z.string().describe("Projected expense amount."),
          percentage: z.string().describe("Percentage of total expenses."),
        })
      ),
      requiredDocuments: z.array(z.string()).describe("List of required financial documents."),
    });

    // Construct the AI prompt
    const prompt = `
      You are an expert financial advisor. Given the following business details, generate a structured financial plan that includes:
      - A step-by-step roadmap for business growth.
      - Revenue projections over different periods.
      - Expense breakdown by category.
      - A list of financial documents required at each stage.

      Business Details:
      - Business Name: ${businessName}
      - Industry: ${industry}
      - Estimated Startup Cost: ${startupCost}
      - Revenue Streams: ${revenueStreams}
      - Operating Expenses: ${operatingExpenses}
      - Funding Sources: ${fundingSources}

      Return only JSON in the following format:
      {
        "roadmap": ["Step 1", "Step 2", ...],
        "revenueProjections": [
          { "period": "Q1 2024", "revenue": "$10,000", "growth": "5%" },
          ...
        ],
        "expenseBreakdown": [
          { "category": "Marketing", "amount": "$2000", "percentage": "10%" },
          ...
        ],
        "requiredDocuments": ["Business License", "Tax Registration", ...]
      }
    `;

    // Call Gemini API
    const result = await generateObject({
      model: google("gemini-1.5-pro"),
      system: "Generate a structured financial plan based on user input.",
      prompt,
      schema,
    });

    return result.toJsonResponse();
  } catch (error) {
    console.error("Error generating financial plan:", error);
    return new Response(JSON.stringify({ error: "Failed to generate financial plan" }), { status: 500 });
  }
}

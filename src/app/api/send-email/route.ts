import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: Request) {
  try {
    const { recipient, subject, body } = await request.json();

    if (!recipient || !subject || !body) {
      return new Response(
        JSON.stringify({ error: "Missing required fields" }),
        { status: 400 }
      );
    }

    const { data, error } = await resend.emails.send({
      from: "Automation Hub <noreply@your_domain.com>",
      to: [recipient],
      subject,
      html: `<p>${body}</p>`,
    });

    if (error) {
      return new Response(
        JSON.stringify({ error: "Failed to send email", details: error }),
        { status: 500 }
      );
    }

    return new Response(
      JSON.stringify({ message: "Email sent successfully" }),
      { status: 200 }
    );
  } catch (error) {
    console.error("Error sending email:", error);
    return new Response(
      JSON.stringify({ error: "Internal Server Error" }),
      { status: 500 }
    );
  }
}

import { Header } from "./header";
import { BackgroundBeams } from "@/components/ui/background-beams";

type Props = {
  children: React.ReactNode;
};

const MarketingLayout = ({ children }: Props) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 flex flex-col items-center justify-between">
        {children}
      </main>
    </div>
  );
};

export default MarketingLayout;
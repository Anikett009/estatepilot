import { Sidebar } from "@/app/components/sidebar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation";
import { BackgroundLines } from "@/components/ui/background-lines";

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    
      <div className="h-full relative">
        <Sidebar />
        <div className="lg:pl-[240px] h-full">
  
          <div className="h-full max-w-[1100px] mx-auto p-6 relative z-10">
      
      
            {children}
          </div>
        </div>
      </div>

  );
};

export default MainLayout;

import { cn } from "@/lib/utils";
import Image from "next/image";
import Link from "next/link";
import { SidebarItem } from "@/app/components/sidebar-item";
import { ClerkLoaded, ClerkLoading, UserButton } from "@clerk/nextjs";
import { Loader } from "lucide-react";

type Props = {
  className?: string;
};

export const Sidebar = ({ className }: Props) => {
  return (
    <div
      className={cn(
        "flex h-full lg:w-[320px] lg:fixed left-0 top-0 px-4 border-r-2 flex-col",
        className
      )}
    >
      <Link href="/dashboard">
        <div className="pt-8 pl-4 pb-7 flex items-center gap-x-3">
          <Image src="/house.png" alt="Mascot" width={40} height={40} />
          <h1 className="text-2xl font-extrabold text-zinc-700 tracking-wide">
            EstateAgent
          </h1>
        </div>
      </Link>

      <div className="flex flex-col gap-y-2 flex-1">
        
        <SidebarItem
          label={"Real Estate Chatbot"}
          iconSrc={"/bulb.png"}
          href={"/validation"}
        />
        <SidebarItem
          label={"Conversations"}
          iconSrc={"/match.png"}
          href={"/deck"}
        />
        <SidebarItem label={"Property Listing"} iconSrc={"/deal.png"} href={"/match"} />
        <SidebarItem label={"Follow - Up"} iconSrc={"/analyser.png"} href={"/elevatorpitch"} />
        <SidebarItem label={"Multilingual Summarizer"} iconSrc={"/automation.png"} href={"/automation"} />
        <SidebarItem
          label={"Profiling"}
          iconSrc={"/bulb.png"}
          href={"/profiling"}
        />
        <SidebarItem
          label={"Ad Generator"}
          iconSrc={"/bulb.png"}
          href={"/adgenerator"}
        />
      
      </div>
      <div className="p-4">
        <ClerkLoading>
          <Loader className="size-5 text-muted-foreground animate-spin" />
        </ClerkLoading>
        <ClerkLoaded>
          <UserButton afterSignOutUrl="/" />
        </ClerkLoaded>
      </div>
    </div>
  );
};
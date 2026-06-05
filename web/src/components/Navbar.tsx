import {
  BookOpenText,
  Check,
  FolderPlus,
  History,
  MoreHorizontal,
  PanelLeft,
  SquarePen,
  Search,
  Wifi,
  X,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

type NavbarProps = {
  onSelectNewChat: () => void;
  apiHost: string;
};

const sidebarItems = [
  { label: "Đoạn chat mới", icon: SquarePen, active: true },
  { label: "Tìm kiếm đoạn chat", icon: Search },
  { label: "Thư viện", icon: BookOpenText },
  { label: "Dự án", icon: FolderPlus },
  { label: "Lịch sử", icon: History },
  { label: "Thêm", icon: MoreHorizontal },
];

const recentChats = [
  "Ôn tập chương 3",
  "Chủ trương của Đảng 1945",
  "Hàng hóa và giá trị",
  "Vật chất và ý thức",
  "Đường lối đổi mới",
  "So sánh cương lĩnh",
  "Kháng chiến chống Pháp",
  "Phép biện chứng",
  "Thị trường và tiền tệ",
  "Bài học kinh nghiệm",
  "Nội dung Đại hội VI",
  "Tồn tại xã hội",
];

export function Navbar({
  onSelectNewChat,
  apiHost,
}: NavbarProps) {
  const { state, setOpen, isMobile, setOpenMobile } = useSidebar();
  const isSidebarOpen = state === "expanded";
  const isExpanded = isMobile ? true : isSidebarOpen;

  return (
    <Sidebar collapsible="icon" className="border-r border-neutral-200 bg-neutral-50">
      {/* Header */}
      <SidebarHeader
        className={`h-16 flex flex-row items-center transition-all duration-300 ${isExpanded ? "justify-between px-3.5" : "justify-center px-0"
          }`}
      >
        <h2
          className={`text-lg font-semibold text-neutral-950 transition-all overflow-hidden whitespace-nowrap ${isExpanded
            ? "max-w-[150px] opacity-100 duration-300 delay-100 ease-out"
            : "max-w-0 opacity-0 pointer-events-none duration-100 ease-in"
            }`}
        >
          RAG Base
        </h2>
        <button
          className="grid size-8 flex-shrink-0 place-items-center rounded-lg text-neutral-600 hover:bg-neutral-200 transition-transform duration-300"
          type="button"
          title={isExpanded ? "Đóng thanh bên" : "Mở thanh bên"}
          onClick={() => isMobile ? setOpenMobile(false) : setOpen(!isSidebarOpen)}
        >
          <X className="md:hidden" size={20} strokeWidth={1.5} />
          <PanelLeft
            className="hidden md:block transition-transform duration-300"
            size={21}
            strokeWidth={1.5}
          />
        </button>
      </SidebarHeader>

      {/* Main Content */}
      <SidebarContent className="px-3.5">
        <SidebarMenu className="gap-1">
          {sidebarItems.map((item) => {
            const Icon = item.icon;
            return (
              <SidebarMenuItem key={item.label}>
                <SidebarMenuButton
                  isActive={item.active}
                  onClick={() => {
                    if (item.label === "Đoạn chat mới") {
                      onSelectNewChat();
                    }
                  }}
                  className={`flex min-h-9 items-center rounded-lg text-sm transition-all duration-300 ${item.active
                    ? "bg-neutral-200 text-neutral-950"
                    : "text-neutral-800 hover:bg-neutral-200"
                    } ${isExpanded ? "w-full px-3 justify-start" : "w-full px-[7px] justify-start"}`}
                >
                  <Icon size={20} strokeWidth={1.5} className="flex-shrink-0" />
                  <span
                    className={`transition-all overflow-hidden whitespace-nowrap ${isExpanded
                      ? "max-w-[200px] opacity-100 ml-3 duration-300 delay-75 ease-out"
                      : "max-w-0 opacity-0 ml-0 pointer-events-none duration-100 ease-in"
                      }`}
                  >
                    {item.label}
                  </span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            );
          })}
        </SidebarMenu>

        {/* Recent Chats Section */}
        <div
          className={`transition-all flex flex-col min-h-0 flex-1 ${isExpanded
            ? "opacity-100 max-h-[1000px] mt-7 duration-300 delay-75 ease-out"
            : "opacity-0 max-h-0 overflow-hidden pointer-events-none mt-0 duration-100 ease-in"
            }`}
        >
          <h3 className="mb-2 px-3 text-sm font-semibold text-neutral-950">Gần đây</h3>
          <div className="min-h-0 flex-1 overflow-y-auto pr-1">
            {recentChats.map((chat) => (
              <button
                className="block min-h-9 w-full truncate rounded-lg px-3 text-left text-sm text-neutral-900 hover:bg-neutral-200"
                key={chat}
                type="button"
              >
                {chat}
              </button>
            ))}
          </div>
        </div>
      </SidebarContent>

      {/* Footer */}
      <SidebarFooter
        className={`flex flex-col border-t border-neutral-200 transition-all duration-300 ${isExpanded ? "p-3.5 gap-3" : "p-3.5 gap-0"
          }`}
      >
        {/* Profile */}
        <div
          className={`flex items-center rounded-lg hover:bg-neutral-200 transition-all duration-300 cursor-pointer w-full justify-start ${isExpanded ? "px-2 py-2" : "px-0 py-2"
            }`}
        >
          <div className="grid size-8 place-items-center rounded-full bg-teal-500 text-[10px] font-bold text-white flex-shrink-0">
            AN
          </div>
          <div
            className={`transition-all overflow-hidden flex items-center justify-between flex-1 whitespace-nowrap ${isExpanded
              ? "max-w-[200px] opacity-100 ml-3 duration-300 delay-75 ease-out"
              : "max-w-0 opacity-0 ml-0 pointer-events-none duration-100 ease-in"
              }`}
          >
            <div className="min-w-0 flex-1 whitespace-nowrap overflow-hidden">
              <p className="truncate text-sm font-medium text-neutral-950">nttzb0930</p>
              <div className="flex items-center gap-1.5 text-xs text-neutral-500 whitespace-nowrap overflow-hidden">
                <Wifi size={12} className="flex-shrink-0" />
                <span className="truncate">{apiHost}</span>
              </div>
            </div>
            <Check size={15} className="text-neutral-500 ml-2 flex-shrink-0" />
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}

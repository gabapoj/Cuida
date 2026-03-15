import { SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { Breadcrumb } from "@/components/breadcrumb"

interface PageTopBarProps {
  title: string
  actions?: React.ReactNode
  children: React.ReactNode
}

export function PageTopBar({ title, actions, children }: PageTopBarProps) {
  return (
    <>
      <header className="group-has-data-[collapsible=icon]/sidebar-wrapper:h-12 flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear">
        <div className="grid w-full grid-cols-3 items-center px-4">
          <div className="flex items-center justify-start gap-2">
            <SidebarTrigger className="-ml-1" />
            <Separator
              orientation="vertical"
              className="mr-2 data-[orientation=vertical]:h-4"
            />
            <Breadcrumb currentPageTitle={title} />
          </div>
          <div className="flex items-center justify-center">
            <h1 className="text-lg font-semibold tracking-tight">{title}</h1>
          </div>
          <div className="flex items-center justify-end gap-2">{actions}</div>
        </div>
      </header>
      {children}
    </>
  )
}

import { useLocation } from "@tanstack/react-router"
import {
  Breadcrumb as BreadcrumbRoot,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

const routeLabels: Record<string, string> = {
  dashboard: "Dashboard",
  clients: "Clients",
  calls: "Calls",
  settings: "Settings",
}

interface BreadcrumbProps {
  currentPageTitle?: string
}

export function Breadcrumb({ currentPageTitle }: BreadcrumbProps) {
  const { pathname } = useLocation()
  const segments = pathname.split("/").filter(Boolean)

  if (segments.length === 0) return null

  return (
    <BreadcrumbRoot>
      <BreadcrumbList>
        {segments.map((segment, index) => {
          const isLast = index === segments.length - 1
          const label = isLast
            ? (currentPageTitle ?? routeLabels[segment] ?? segment)
            : (routeLabels[segment] ?? segment)

          return (
            <span key={segment} className="flex items-center gap-1.5">
              {index > 0 && <BreadcrumbSeparator />}
              <BreadcrumbItem>
                <BreadcrumbPage>{label}</BreadcrumbPage>
              </BreadcrumbItem>
            </span>
          )
        })}
      </BreadcrumbList>
    </BreadcrumbRoot>
  )
}

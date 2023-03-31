import Link from "next/link"

interface ISideBarLink {
  text: string
  href: string
  page: string
}

export const SideBarLink = ({ text, href, page }: ISideBarLink) => {

  return (
    <Link
      className={`hover:font-bold 
      ${page === "/statistics" && text === "Statistics" ? "font-bold" : ""}
      ${page === "/information" && text === "Information" ? "font-bold" : ""}
      ${page === "/" && text === "Home" ? "font-bold" : ""}
      `}
      href={href}
    >
      {text}{" "}
    </Link>
  )
}

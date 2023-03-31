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
      ${page === "/other_page" && text === "Other page" ? "font-bold" : ""}
      ${page === "/about_us" && text === "About us" ? "font-bold" : ""}
      ${page === "/" && text === "Home" ? "font-bold" : ""}
      `}
      href={href}
    >
      {text}{" "}
    </Link>
  )
}

/* eslint-disable tailwindcss/no-contradicting-classname */
/* eslint-disable @next/next/no-img-element */
import { Page } from "../components/Page"
import { Header } from "../components/Header"
import { ResponsiveText } from "../components/ReponsiveText"
import { useEffect } from "react"
import { getRequest } from "../src/functions/api/get"
import { useState } from "react"
import { useTranslation } from "react-i18next"
import { useSelector } from "react-redux"
import axios from "axios"
import clsx from "clsx"

export default function OtherPage () {

  const [bootTime, setBootTime] = useState<string>("")
  const [version, setVersion] = useState<string>("")
  const [numberOfCommits, setNumberOfCommits] = useState<string>("")
  const [lastCommit, setLastCommit] = useState<string>("")
  const [ramUsage, setRamUsage] = useState<string>("")
  const [cpuLoad, setCpuLoad] = useState<string>("")
  const [discUsage, setDiscUsage] = useState<string>("")
  const [topProgrammer, setTopProgrammer] = useState<any>({})
  const [longTermData, setLongTermData] = useState<any>({commits_by_date:[]})
  const mode = useSelector((state: any) => state.mode)
  const {t} = useTranslation()
  const apiUrl = "https://tda.knapa.cz/user"

  useEffect(() => {
    const initialInterval = async () =>{
      const uptimeData = await getRequest("/basics/uptime")
      const basicsData = await getRequest("/basics/commits")
      const monitorData = await getRequest("/monitor/info")
      const topProgrammerId = await getRequest("/bacics/topProgrammer")
      const longTermData = await getRequest("/longStats/commitsByDate")
      const topProgrammer = await axios.get(`${apiUrl}/${topProgrammerId.top_programmer}`, {
        headers: {
          "x-access-token": "9492a5fdccb71211fed377fcd8d47508", 
        }
      })
      console.log(longTermData)
      setLongTermData(longTermData)
      setTopProgrammer(topProgrammer.data)
      setCpuLoad(monitorData.cpu_load)
      setRamUsage(monitorData.ram_usage)
      setDiscUsage(monitorData.disk_usage)
      setNumberOfCommits(basicsData.count)
      setLastCommit(basicsData.last.description)
      setBootTime(uptimeData.boot_time)
      setVersion(uptimeData.platform)

    }
    initialInterval()

    const regularInterval = setInterval(async () => {
      const uptimeData = await getRequest("/basics/uptime")
      const basicsData = await getRequest("/basics/commits")
      const monitorData = await getRequest("/monitor/info")
      const topProgrammerId = await getRequest("/bacics/topProgrammer")
      const topProgrammer = await axios.get(`${apiUrl}/${topProgrammerId.top_programmer}`, {
        headers: {
          "x-access-token": "9492a5fdccb71211fed377fcd8d47508", 
        }
      })
      setTopProgrammer(topProgrammer.data)
      setCpuLoad(monitorData.cpu_load)
      setRamUsage(monitorData.ram_usage)
      setDiscUsage(monitorData.disk_usage)
      setNumberOfCommits(basicsData.count)
      setLastCommit(basicsData.last.description)
      setBootTime(uptimeData.boot_time)
      setVersion(uptimeData.platform)
    }, 30000)
    
    return () => clearInterval(regularInterval)
  }, [])

  const HalfContainer = ({children, className}:{children:any, className?:string})=>{
    return(
      <div className={clsx("h-[250px] w-[50%] p-10",mode?"border border-white":"border border-black",className)}>
        {children}
      </div>
    )
  }

  return (
    <Page>
      <title>Sticknotes | Statistics</title>
      <Header />
      <div className="flex w-full">
        <HalfContainer>
          <ResponsiveText className="text-center text-2xl font-bold">
            {t("basic_commits")}:
          </ResponsiveText><br/>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">{t("number_of_commits")}: </span> {numberOfCommits}
          </ResponsiveText>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">{t("Last_commit")}:</span> {lastCommit}
          </ResponsiveText>
        </HalfContainer>
        <HalfContainer>
          <div className="flex"></div>
          <ResponsiveText className="text-center text-2xl font-bold">
            {t("Uptime")}
          </ResponsiveText><br/>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">{t("Boot_time")}: </span> {bootTime}
          </ResponsiveText>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">{t("System_version")}:</span> {version}
          </ResponsiveText>
        </HalfContainer>
      </div>
      <div className="flex">
        <HalfContainer className="h-[400px]">
          <div className="flex w-full">
            <div className="mx-auto mb-2 flex h-fit">
              <ResponsiveText className="pt-[4px] text-2xl font-bold">
                {t("Winner")}
              </ResponsiveText>
              <img className="m-auto ml-2 h-[40px]" alt="" src={"king.png"} />
            </div><br/>
          </div>
          <ResponsiveText className="text-center text-2xl">
            {topProgrammer.name}
          </ResponsiveText>
          <div className="flex w-full">
            <img className="m-auto mt-5" alt="" src={topProgrammer.avatar_url}/>
          </div>
        </HalfContainer>
        <HalfContainer className="h-[400px]">
          <ResponsiveText className="text-center text-2xl font-bold">
            {t("Usage")}
          </ResponsiveText><br/>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">CPU:</span> {cpuLoad}%
          </ResponsiveText>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">RAM:</span> {ramUsage}%
          </ResponsiveText>
          <ResponsiveText className="text-center text-xl">
            <span className="font-bold">{t("Disc")}:</span> {discUsage}%
          </ResponsiveText>
        </HalfContainer>
      </div>
      <div className={clsx("flex w-fit w-full flex-wrap gap-10 p-10",!mode?"border border-black":"border border-white")}>
        <ResponsiveText className="w-full text-center text-2xl font-bold">
          {t("Graph")}
        </ResponsiveText><br/>
        {longTermData.commits_by_date.map((item:any)=>{
          return(
            <div className="h-[300px] w-max" key={item.date}>
              <ResponsiveText>
                {item.date}
              </ResponsiveText>
              {Array.from({ length: item.value }).map((_, i) => (
                <div className="h-[3px] bg-[#0000FF]" key={i}/>
              ))}
            </div>
          )
        })}
      </div>
    </Page>
  )
}
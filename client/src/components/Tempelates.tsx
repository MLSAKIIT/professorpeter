import { cn } from '@/lib/utils'
import React from 'react'
import DecryptedText from './ui/DecryptedText'

const Tempelates = () => {
  return (
    <div className="relative flex h-[50rem] w-full  bg-black dark:bg-black">
      <div
        className={cn(
          "absolute inset-0",
          "[background-size:40px_40px]",
          "[background-image:linear-gradient(to_right,#262626_1px,transparent_1px),linear-gradient(to_bottom,#262626_1px,transparent_1px)]",
          "dark:[background-image:linear-gradient(to_right,#262626_1px,transparent_1px),linear-gradient(to_bottom,#262626_1px,transparent_1px)]",
        )}
      />
      <div className="pointer-events-none absolute inset-0 flex  justify-center bg-black [mask-image:radial-gradient(ellipse_at_center,transparent_5%,black)] dark:bg-black"></div>
      <div className='relative z-20 w-full flex flex-col px-4 pt-16'>
        <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold text-center 
                      bg-clip-text text-transparent 
                      bg-gradient-to-r from-[#c0c0c0] via-[#e8e8e8] to-[#9a9a9a] 
                      animate-shimmer bg-[length:200%_100%]
                      py-4 drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.5)]">
          Pick a template. Type nonsense. Watch Peter struggle to explain it.
        </h1>
      </div>
      <div>
      </div>
    </div>
  )
}

export default Tempelates
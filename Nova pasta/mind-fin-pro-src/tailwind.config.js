/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html","./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        mfp:{
          bg:"#0B0E14", card:"#11151D", stroke:"#1C2230",
          primary:"#3AA0FF", accent:"#EAC65C", text:"#E6EDF7", muted:"#95A2B3",
          good:"#37D67A", warn:"#FFB020", bad:"#FF5A5F", info:"#5AC8FA"
        }
      },
      boxShadow:{ soft:"0 8px 30px rgba(0,0,0,.35)" },
      borderRadius:{ xl2:"1.25rem" },
      keyframes:{
        fadeup:{ "0%":{opacity:"0", transform:"translateY(6px) scale(.98)"},
                 "100%":{opacity:"1", transform:"translateY(0) scale(1)"} }
      },
      animation:{ fadeup:"fadeup .4s ease forwards" }
    }
  },
  plugins:[]
}

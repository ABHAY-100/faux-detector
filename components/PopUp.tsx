import Image from "next/image";

function PopUp() {
    
    
  return (
    <>
      <div
        id="popup"
        className="w-[200px] h-[300px] flex items-center justify-center gap-3 flex-col"
      >
        <Image id="icon" src="icon.png" alt="" />

        <section className="flex items-center justify-center flex-col gap-3">
          <button
            id="button-on"
            className="button p-3 rounded-sm border-gray-400"
          >
            ON
          </button>
          <button
            id="button-off"
            className="button p-3 rounded-sm border-gray-400"
          >
            OFF
          </button>
        </section>
      </div>
    </>
  );
}

export default PopUp;

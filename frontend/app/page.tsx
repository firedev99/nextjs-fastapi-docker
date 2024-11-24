import { Form } from "@/components";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div>
          <div className="text-center mb-5">
            <h1 className="text-5xl font-bold">Create New Account</h1>
            <p className="mt-2 text-md opacity-70">testing endpoint <span className="bg-red-500 text-black px-2 py-1 rounded-sm text-base">/api/v1/auth/signup</span></p>
          </div>
          <Form />
        </div>
      </main>
    </div>
  );
}


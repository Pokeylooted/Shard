import path from "node:path"
import { fileURLToPath } from "node:url"
import dotenv from "dotenv"

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

dotenv.config({ path: path.join(__dirname, "../../.env") })

const { FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_USERNAME, FIRST_SUPERUSER_PASSWORD } = process.env

if (typeof FIRST_SUPERUSER_EMAIL !== "string") {
  throw new Error("Environment variable FIRST_SUPERUSER_EMAIL is undefined")
}

if (typeof FIRST_SUPERUSER_USERNAME !== "string") {
  throw new Error("Environment variable FIRST_SUPERUSER_USERNAME is undefined")
}

if (typeof FIRST_SUPERUSER_PASSWORD !== "string") {
  throw new Error("Environment variable FIRST_SUPERUSER_PASSWORD is undefined")
}

export const firstSuperuserEmail = FIRST_SUPERUSER_EMAIL as string
export const firstSuperuserUsername = FIRST_SUPERUSER_USERNAME as string
export const firstSuperuserPassword = FIRST_SUPERUSER_PASSWORD as string

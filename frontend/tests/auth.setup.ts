import { test as setup } from "@playwright/test"
import { firstSuperuserPassword, firstSuperuserUsername } from "./config.ts"

const authFile = "playwright/.auth/user.json"

setup("authenticate", async ({ page }) => {
  await page.goto("/login")
  await page.getByPlaceholder("Username").fill(firstSuperuserUsername)
  await page.getByPlaceholder("Password").fill(firstSuperuserPassword)
  await page.getByRole("button", { name: "Log In" }).click()
  await page.waitForURL("/")
  await page.context().storageState({ path: authFile })
})

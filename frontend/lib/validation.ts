import { z } from "zod";

export const EmployeeFormValidation = z.object({
    phone: z.string().refine((phone) => /^\+\d{10,15}$/.test(phone), 'Некорретный формат номера'),
})
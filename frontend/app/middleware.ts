import { NextResponse, NextRequest } from "next/server";

export function middleware(req: NextRequest) {
    const accessToken = req.cookies.get('access_token');
    if (!accessToken) {
        return NextResponse.redirect(new URL('/', req.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/admin/:path*', '/company/:path*', '/office/:path*'],
};
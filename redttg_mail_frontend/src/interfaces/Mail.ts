interface Envelope {
    from: string
    to: string[]
}

interface PreviewAttachment {
    id: number
    filename: string
    type: string
}

interface Attachment extends PreviewAttachment {
    file: string
}

export interface MailPreview {
    id: number
    subject: string
    created: Date
    envelope: Envelope
    read: boolean
    attachments: PreviewAttachment[]
}

export interface Mail extends MailPreview {
    text: string
    html: string
    from_sender: string
    star: boolean
    deleted: boolean
    attachments: Attachment[]
}
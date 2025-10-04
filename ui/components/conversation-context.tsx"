"use client";

import { PanelSection } from "./panel-section";
import { Card, CardContent } from "@/components/ui/card";
import { BookText } from "lucide-react";

interface ConversationContextProps {
  context: {
    customer_name?: string;
    customer_email?: string;
    customer_phone?: string;
    project_number?: string;
    project_type?: string;
    construction_type?: string;
    area_sqm?: number;
    location?: string;
    budget_chf?: number;
    preferred_start_date?: string;
    consultation_booked?: boolean;
    specialist_assigned?: string;
    inquiry_id?: string;
  };
}

export function ConversationContext({ context }: ConversationContextProps) {
  return (
    <PanelSection
      title="Conversation Context"
      icon={<BookText className="h-4 w-4 text-[#928472]" />}
    >
      <Card className="bg-gradient-to-r from-white to-gray-50 border-gray-200 shadow-sm">
        <CardContent className="p-3">
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(context).map(([key, value]) => (
              <div
                key={key}
                className="flex items-center gap-2 bg-white p-2 rounded-md border border-gray-200 shadow-sm transition-all"
              >
                <div className="w-2 h-2 rounded-full bg-[#928472]"></div>
                <div className="text-xs">
                  <span className="text-zinc-500 font-light">{key}:</span>{" "}
                  <span
                    className={
                      value !== null && value !== undefined
                        ? "text-zinc-900 font-light"
                        : "text-gray-400 italic"
                    }
                  >
                    {value !== null && value !== undefined ? String(value) : "null"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </PanelSection>
  );
}
import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent from "@mui/lab/TimelineContent";
import TimelineDot from "@mui/lab/TimelineDot";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
import { Typography } from "@mui/material";

export default function TimelineStart() {
	return (
		<TimelineItem>
			<TimelineOppositeContent
				sx={{ m: "auto 0" }}
				align="right"
				variant="body2"
				color="text.secondary"
			>
				<Typography variant="body2">0 secs</Typography>
			</TimelineOppositeContent>
			<TimelineSeparator>
				<TimelineConnector />
				<TimelineDot />
				<TimelineConnector />
			</TimelineSeparator>
			<TimelineContent sx={{ py: "30px", px: 4 }}>
				<Typography variant="h6" component="span">
					Start of Game
				</Typography>
			</TimelineContent>
		</TimelineItem>
	);
}

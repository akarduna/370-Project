import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent from "@mui/lab/TimelineContent";
import TimelineDot from "@mui/lab/TimelineDot";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
import { Avatar, Typography } from "@mui/material";
import TakedownIcon from "../images/takedownIcon.png";

export default function TimelineTakedown({ heartrate, enemy, time }) {
	return (
		<TimelineItem>
			<TimelineOppositeContent
				sx={{ m: "auto 0" }}
				align="right"
				variant="body2"
				color="text.secondary"
			>
				<Typography>{heartrate} bpm</Typography>
				<Typography>{time}</Typography>
			</TimelineOppositeContent>
			<TimelineSeparator>
				<TimelineConnector />
				<TimelineDot>
					<Avatar alt="Takedown" src={TakedownIcon} />
				</TimelineDot>
				<TimelineConnector />
			</TimelineSeparator>
			<TimelineContent sx={{ py: "30px", px: 4 }}>
				<Typography variant="h6" component="span">
					Takedown
				</Typography>
				<Typography>{enemy}</Typography>
			</TimelineContent>
		</TimelineItem>
	);
}
